# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from itdevice.models import *
from django.shortcuts import render_to_response
from django.contrib import messages
import datetime
from django.contrib.sessions.models import Session
import pandas as pd
from sqlalchemy import create_engine
import os
import csv
from pandas import ExcelWriter
from django.http import HttpResponseRedirect
from forms import *
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

mysql_cnxn = create_engine('mysql+mysqldb://root:kevin6102531@localhost:3306/pcc?charset=utf8')
output_time = ""

@login_required(login_url='/accounts/login/')
def index(request):
    global output_time
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.filter(dept_parent="")
    all_type = Type.objects.all()
    all_itdevice = Itdevice.objects.all()
    all_material = Material.objects.all()    
    if request.session.has_key('output_time'):
        output_time = request.session.get('output_time')

    context = {'all_device':all_itdevice,'all_type':all_type,'all_dept':all_dept,'deptparent':deptparent,'all_material':all_material, 'output_time':output_time}
    return  render(request,'itdevice/index.html',context)

def parse_date(td):
    resYear = float(td.days)/364.0                   # get the number of years including the the numbers after the dot
    resMonth = int((resYear - int(resYear))*364/30)  # get the number of months, by multiply the number after the dot by 364 and divide by 30.
    resYear = int(resYear)
    return str(resYear) + "Y" + str(resMonth) + "m"

@login_required(login_url='/accounts/login/')
def asset_cal(request):
    script_path = os.path.dirname(__file__)
    output_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    review_order = request.POST['review_options']
    csvfile = request.FILES['csv_file'] 
    df_itdevice_new_id_list = []
    
    try:
        # df_itdevice_new_id = pd.read_csv(csvfile)
        if csvfile.name.split('.')[-1] == 'csv':
            df_itdevice_new_id_list = []
            reader = csv.reader(csvfile)
            print csvfile
            for row in reader:
                print row[0]
                df_itdevice_new_id_list.append(row[0])
            print df_itdevice_new_id_list
            print 'is csv'
        elif csvfile.name.split('.')[-1] == 'xlsx':
            df = pd.read_excel(csvfile, header=None, index_col=None)
            df_itdevice_new_id_list = df[0].astype(str).tolist()
            print 'is xlsx'
        else:
            print 'this file is not csv or xlsx...'
            print 'test   something wrong...'
            messages.error(request, 'NO')
            return HttpResponseRedirect("/itdevice/")

        itdevice_sql = ('SELECT * FROM fixed_asset.itdevice')
        df_itdevice = pd.read_sql(itdevice_sql, mysql_cnxn) 
        material_sql = ('SELECT * FROM fixed_asset.material')
        df_material = pd.read_sql(material_sql, mysql_cnxn) 
        type_sql = ('SELECT * FROM fixed_asset.type')
        df_type = pd.read_sql(type_sql, mysql_cnxn) 
        manager_sql = ('SELECT * FROM fixed_asset.dept')
        df_manager = pd.read_sql(manager_sql, mysql_cnxn) 
        itdevice_sql = ('SELECT * FROM fixed_asset.itdevice')
        df_itdevice = pd.read_sql(itdevice_sql, mysql_cnxn) 
        df_itdevice = df_itdevice.merge(df_material, how='left', on=['material_id']).merge(df_type, how='left', on=['type_id']).merge(df_manager, how='left', on=['dept_id'])
        
        df_itdevice['pur_date'] = df_itdevice['pur_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df_itdevice['today_date'] = datetime.datetime.today().strftime("%Y-%m-%d")
        df_itdevice['delta'] = [parse_date(datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.datetime.strptime(end, '%Y-%m-%d')) for start, end in zip(df_itdevice['today_date'], df_itdevice['pur_date'])]
        
        scan_dept_list = list(set(df_itdevice[df_itdevice.device_id.isin(df_itdevice_new_id_list)]['dept_id'].astype(str).tolist()))
        print scan_dept_list
        df_itdevice_new = df_itdevice[df_itdevice.dept_id.isin(scan_dept_list)]
        device_in_dept_list = df_itdevice[df_itdevice.dept_id.isin(scan_dept_list)]['device_id'].astype(str).tolist()
        total_device_num = len(df_itdevice[df_itdevice.dept_id.isin(scan_dept_list)])
        print total_device_num
        not_match_list = list(set(device_in_dept_list) - set(df_itdevice_new_id_list))
        df_itdevice_new['first_review'] = ""
        df_itdevice_new['second_review'] = ""
        df_itdevice_new['sign'] = ''
        df_itdevice_new = df_itdevice_new.reset_index(drop=True)
        df_itdevice_new['id'] = df_itdevice_new.index +1
        df_itdevice_new = df_itdevice_new[['id','user_name','typename','device_id','materialname','dept_id','manager','first_review','second_review','sign','delta']]
        total_device_scan_dept = len(df_itdevice_new[df_itdevice_new.dept_id.isin(scan_dept_list)])
        if review_order == 'First Review':
            df_itdevice_new['first_review'] = "YES"
            df_itdevice_new.loc[df_itdevice_new.device_id.isin(not_match_list), 'first_review'] = "NO"
            # df_itdevice_new_not_match = df_itdevice_new[df_itdevice_new['first_review'] == 'NO']
            not_match_num = len(df_itdevice_new[df_itdevice_new.first_review == 'NO'])
            match_num = len(df_itdevice_new) - not_match_num
        if review_order == 'Second Review':
            df_itdevice_new['second_review'] = "YES"
            df_itdevice_new.loc[df_itdevice_new.device_id.isin(not_match_list), 'second_review'] = "NO"
            # df_itdevice_new_not_match = df_itdevice_new[df_itdevice_new['second_review'] == 'NO']
            not_match_num = len(df_itdevice_new[df_itdevice_new.first_review == 'NO'])
            match_num = len(df_itdevice_new) - not_match_num

        previous_folder = "\\".join(script_path.split('\\')[:-1])
        # writer0 = ExcelWriter(previous_folder + '\\static\\output_not_match.xlsx')
        print df_itdevice_new
        writer = ExcelWriter(previous_folder + '\\static\\output1.xlsx')
        print '1'
        # df_itdevice.columns = ['序號(STT)','使用者(Người dùng)','資產類別(Asset Type)','資產編碼(Ma Tai San)','資產名稱(Asset Name)','存放部門(Bộ phận SD)','管理人(Người Ql)','初盤(Sơ Kiểm)','複盤(Kiểm Lại)','簽名(Ký tên)','備註(Ghi chú)']
        df_itdevice_new.columns = ['序號(STT)','使用者(Người dùng)','資產類別(Asset Type)','資產編碼(Ma Tai San)','資產名稱(Asset Name)','存放部門(Bộ phận SD)','管理人(Người Ql)','初盤(Sơ Kiểm)','複盤(Kiểm Lại)','簽名(Ký tên)','備註(Ghi chú)']
        df_itdevice_new.to_excel(writer,'not_match',index=False)
        print '2'
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "AD"].to_excel(writer,'AD',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "BM"].to_excel(writer,'BM',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "CO"].to_excel(writer,'CO',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "DVC"].to_excel(writer,'DVC',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "DVG"].to_excel(writer,'DVG',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E1"].to_excel(writer,'E1',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E2"].to_excel(writer,'E2',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E3"].to_excel(writer,'E3',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E4"].to_excel(writer,'E4',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E5"].to_excel(writer,'E5',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "E6"].to_excel(writer,'E6',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "F1"].to_excel(writer,'F1',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "F2"].to_excel(writer,'F2',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "F3"].to_excel(writer,'F3',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "F4"].to_excel(writer,'F4',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "FI"].to_excel(writer,'FI',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "GA"].to_excel(writer,'GA',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "GMO"].to_excel(writer,'GMO',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "HR"].to_excel(writer,'HR',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "IE"].to_excel(writer,'IE',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "IT"].to_excel(writer,'IT',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "MW"].to_excel(writer,'MW',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "NO"].to_excel(writer,'NO',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "PCCO"].to_excel(writer,'PCCO',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "PL"].to_excel(writer,'PL',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "POD"].to_excel(writer,'POD',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "PP"].to_excel(writer,'PP',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "PU"].to_excel(writer,'PU',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "QA"].to_excel(writer,'QA',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "SR"].to_excel(writer,'SR',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "TA"].to_excel(writer,'TA',index=False)
        # df_itdevice[df_itdevice['存放部門(Bộ phận SD)'] == "TB"].to_excel(writer,'TB',index=False)

        print '3'
        # writer0.save()
        writer.save()
        print '4'
        messages.error(request, 'Scan Dept: ' + ', '.join(scan_dept_list) + ', ' + 'Match: ' + str(match_num) + ', ' + 'NotMatch: ' + str(not_match_num))
        request.session['output_time'] = output_time
        return HttpResponseRedirect("/itdevice/")
    except:
        print 'something wrong...'
        messages.error(request, 'NO')
        return HttpResponseRedirect("/itdevice/")

def log(request):
    all_log = AuditlogLogentry.objects.all().order_by('-timestamp')
    all_user = AuthUser.objects.all()
    all_itdevice = Itdevice.objects.all()
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.filter(dept_parent="")
    all_material = Material.objects.all()
    context = {'all_device':all_itdevice,'all_user':all_user,'all_log':all_log,'all_material':all_material,'all_dept':all_dept,'deptparent':deptparent}
    return  render(request,'itdevice/log.html',context)

def dept_filter(request,dept_id):
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.filter(dept_parent="")
    all_type = Type.objects.all()
    all_itdevice = Itdevice.objects.filter(dept_id=dept_id)
    context = {'all_device':all_itdevice,'all_type':all_type,'all_dept':all_dept,'deptparent':deptparent}
    return  render(request,'itdevice/index.html',context)

def date_filter(request,start_date,end_date):
    try:
        all_dept = Dept.objects.all()
        deptparent = Dept.objects.filter(dept_parent="")
        all_type = Type.objects.all()
        all_itdevice = Itdevice.objects.filter(pur_date__gte=start_date, pur_date__lte=end_date)
    except:
        return HttpResponseRedirect("/itdevice/")
    context = {'all_device':all_itdevice,'all_type':all_type,'all_dept':all_dept,'deptparent':deptparent}
    return  render(request,'itdevice/index.html',context)

@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_itdevice(request):
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.filter(dept_parent="")
    all_type = Type.objects.all()
    all_itdevice = Itdevice.objects.all()
    all_material = Material.objects.all()
    context = {'all_device': all_itdevice, 'all_type': all_type, 'all_dept': all_dept, 'deptparent': deptparent,
               'all_material': all_material}
    if request.method == 'POST' and 'save' in request.POST:
        form = ItdeviceForm(request.POST)
        if form.is_valid():
           new_device = form.save()
           return HttpResponseRedirect("/itdevice/")
        else:
            content = {'form':form};
            return render(request, 'itdevice/adddevice.html', content)  
    if request.method == 'POST' and 'add_material' in request.POST:
        return HttpResponseRedirect("/itdevice/addmaterial/")         
    if request.method == 'POST' and 'edit_material' in request.POST:
        selected_value = request.POST["material"] 
        return HttpResponseRedirect("/itdevice/editmaterial/"+selected_value)
    if request.method == 'POST' and 'delete_material' in request.POST:
        selected_value = request.POST["material"] 
        return HttpResponseRedirect("/itdevice/deletematerial/"+selected_value)
    if request.method == 'POST' and 'add_dept' in request.POST:
        return HttpResponseRedirect("/itdevice/adddept/")         
    if request.method == 'POST' and 'edit_dept' in request.POST:
        selected_value = request.POST["dept"] 
        return HttpResponseRedirect("/itdevice/editdept/"+selected_value)
    if request.method == 'POST' and 'delete_dept' in request.POST:
        selected_value = request.POST["dept"] 
        return HttpResponseRedirect("/itdevice/deletedept/"+selected_value)          
    else:
        return render(request, 'itdevice/adddevice.html', context)

@login_required(login_url='/accounts/login/')
@csrf_exempt
def edit_device(request,device_id):
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.all()
    all_type = Type.objects.all()
    all_itdevice = Itdevice.objects.filter(device_id=device_id)
    all_material = Material.objects.all()
    context = {'all_device': all_itdevice, 'all_type': all_type, 'all_dept': all_dept, 'deptparent': deptparent,
               'all_material': all_material}
    if request.method == 'POST' and 'save' in request.POST:
        instance = Itdevice.objects.get(device_id=device_id)
        form = ItdeviceForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/itdevice/")
    if request.method == 'POST' and 'add_material' in request.POST:
        return HttpResponseRedirect("/itdevice/addmaterial/")         
    if request.method == 'POST' and 'edit_material' in request.POST:
        selected_value = request.POST["material"] 
        return HttpResponseRedirect("/itdevice/editmaterial/"+selected_value)
    if request.method == 'POST' and 'delete_material' in request.POST:
        selected_value = request.POST["material"] 
        return HttpResponseRedirect("/itdevice/deletematerial/"+selected_value)
    if request.method == 'POST' and 'add_dept' in request.POST:
        return HttpResponseRedirect("/itdevice/adddept/")         
    if request.method == 'POST' and 'edit_dept' in request.POST:
        selected_value = request.POST["dept"] 
        return HttpResponseRedirect("/itdevice/editdept/"+selected_value)
    if request.method == 'POST' and 'delete_dept' in request.POST:
        selected_value = request.POST["dept"] 
        return HttpResponseRedirect("/itdevice/deletedept/"+selected_value)                
    else:
        return render(request, 'itdevice/editdevice.html', context)        

@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_device(request, device_id):
    delete = Itdevice.objects.get(device_id=device_id)
    if request.method == 'POST'and 'yes' in request.POST:
        form = ItdeviceForm(request.POST, instance=delete)
        delete.delete()
        return HttpResponseRedirect("/itdevice/")    
    if request.method == 'POST'and 'cancel' in request.POST:
        return HttpResponseRedirect("/itdevice/")          
    else:
        return render(request, 'itdevice/deleteconfirm.html')

@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_material(request):
    all_type = Type.objects.all()
    context = {'all_type': all_type}
    if request.method == 'POST' and 'save' in request.POST:
        form = MaterialForm(request.POST)
        if form.is_valid():
            new_material = form.save()
            return redirect('/itdevice')
        else:
            content = {'form':form};
            return render(request, 'itdevice/addmaterial.html', content) 
    if request.method == 'POST' and 'add_type' in request.POST:
        return HttpResponseRedirect("/itdevice/addtype/")         
    if request.method == 'POST' and 'edit_type' in request.POST:
        selected_value = request.POST["type"] 
        return HttpResponseRedirect("/itdevice/edittype/"+selected_value)
    if request.method == 'POST' and 'delete_type' in request.POST:
        selected_value = request.POST["type"] 
        return HttpResponseRedirect("/itdevice/deletetype/"+selected_value)        
    else:
        return render(request, 'itdevice/addmaterial.html', context)

@login_required(login_url='/accounts/login/')
@csrf_exempt
def edit_material(request,material_id):
    all_dept = Dept.objects.all()
    all_type = Type.objects.all()    
    all_material = Material.objects.filter(material_id=material_id)
    context = {'all_type': all_type, 'all_dept': all_dept,'all_material': all_material}
    if request.method == 'POST' and 'save' in request.POST:
        instance = Material.objects.get(material_id=material_id)
        form = MaterialForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/itdevice/")
    if request.method == 'POST' and 'add_type' in request.POST:
        return HttpResponseRedirect("/itdevice/addtype/")         
    if request.method == 'POST' and 'edit_type' in request.POST:
        selected_value = request.POST["type"] 
        return HttpResponseRedirect("/itdevice/edittype/"+selected_value)
    if request.method == 'POST' and 'delete_type' in request.POST:
        selected_value = request.POST["type"] 
        return HttpResponseRedirect("/itdevice/deletetype/"+selected_value)        
    else:
        return render(request, 'itdevice/editmaterial.html', context)


@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_material(request, material_id):
    delete = Material.objects.get(material_id=material_id)
    if request.method == 'POST'and 'yes' in request.POST:
        form = MaterialForm(request.POST, instance=delete)
        delete.delete()
        return HttpResponseRedirect("/itdevice/")
    if request.method == 'POST'and 'cancel' in request.POST:
        return HttpResponseRedirect("/itdevice/")     
    else:
        return render(request, 'itdevice/deleteconfirm.html')


@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_dept(request):
    all_dept = Dept.objects.all()
    context = {'all_dept': all_dept}
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid():
            new_type = form.save()
            return HttpResponseRedirect("/itdevice/")
        else:
            content = {'form':form};
            return render(request, 'itdevice/adddept.html', content)   
    else:
        return render(request, 'itdevice/adddept.html', context)


@login_required(login_url='/accounts/login/')
@csrf_exempt
def edit_dept(request,dept_id):
    filter_dept = Dept.objects.filter(dept_id=dept_id)
    all_dept = Dept.objects.all()
    context = {'all_dept': all_dept,'filter_dept': filter_dept}
    if request.method == 'POST':
        instance = Dept.objects.get(dept_id=dept_id)
        form = DeptForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/itdevice/")
    else:
        return render(request, 'itdevice/editdept.html', context)


@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_dept(request, dept_id):
    delete = Dept.objects.get(dept_id=dept_id)
    if request.method == 'POST'and 'yes' in request.POST:
        form = DeptForm(request.POST, instance=delete)
        delete.delete()
        return HttpResponseRedirect("/itdevice/")
    if request.method == 'POST'and 'cancel' in request.POST:
        return HttpResponseRedirect("/itdevice/")     
    else:
        return render(request, 'itdevice/deleteconfirm.html')


@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            new_type = form.save()
            return HttpResponseRedirect("/itdevice/")
        else:
            content = {'form':form};
            return render(request, 'itdevice/addtype.html', content)    
    else:
        template = loader.get_template('itdevice/addtype.html')
        return HttpResponse(template.render())

@login_required(login_url='/accounts/login/')
@csrf_exempt
def edit_type(request,type_id):
    all_type = Type.objects.filter(type_id=type_id)
    context = {'all_type': all_type}
    if request.method == 'POST':
        instance = Type.objects.get(type_id=type_id)
        form = TypeForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/itdevice/")
    else:
        return render(request, 'itdevice/edittype.html', context)


@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_type(request, type_id):
    delete = Type.objects.get(type_id=type_id)
    if request.method == 'POST'and 'yes' in request.POST:
        form = TypeForm(request.POST, instance=delete)
        delete.delete()
        return HttpResponseRedirect("/itdevice/")
    if request.method == 'POST'and 'cancel' in request.POST:
        return HttpResponseRedirect("/itdevice/")     
    else:
        return render(request, 'itdevice/deleteconfirm.html')


class UserFormView(View):
    form_class = UserForm
    template_name ='itdevice/registration_form.html'

@login_required(login_url='/accounts/login/')
@csrf_exempt
def import_file(request):
    all_inventory = Inventory.objects.all()
    all_inventory_type = InventoryType.objects.all()
    context = {'all_inventory': all_inventory,'all_inventory_type': all_inventory_type}
    if request.method == 'POST':
 #       with open(request.FILES['file'],'r') as f:
        with open('static/filename.txt','r') as f:    
            text = f.readlines()
            for line in text:
                p = Importfile(i_id=request.POST.get('i'),i_type_id=request.POST.get('i_type'),lable=line.strip(' \t\n\r'),date=datetime.datetime.now())           
                p.save()
            return HttpResponseRedirect("/itdevice/inventory")
    else:
        return render(request, 'itdevice/import.html', context)


@login_required(login_url='/accounts/login/')
def inventory(request):
    all_dept = Dept.objects.all()
    deptparent = Dept.objects.filter(dept_parent="")
    all_type = Type.objects.all()
    all_itdevice = Itdevice.objects.all()
    all_material = Material.objects.all()  
    all_importfile = Importfile.objects.all()   
    context = {'all_device':all_itdevice,'all_type':all_type,'all_dept':all_dept,'deptparent':deptparent,'all_material':all_material,'all_importfile':all_importfile}
    return  render(request,'itdevice/inventory.html',context)
