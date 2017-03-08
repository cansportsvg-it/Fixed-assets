from django import  template
from itdevice.models import *
from datetime import datetime
from datetime import timedelta

register = template.Library()

@register.filter
def getChilds(dept_parent):
    return  Dept.objects.filter(dept_parent=dept_parent)


@register.filter
def hasChilds(dept_parent):
    childs =  Dept.objects.filter(dept_parent=dept_parent)
    if (childs is not None):
        if (len(childs) > 0):
            return "True"
    return "False"

@register.filter
def tinh(pur_date):
    year =  int((datetime.now().date() - pur_date).days / 365.25)
    month = int((datetime.now().date() - pur_date).days % 365 / 30)
    return str(year)+" years "+str(month)+" months"

@register.filter
def Firstcheck(device_id):
    lable =  Importfile.objects.filter(lable=device_id , i_type=1)
    if (lable is not None):
        if (len(lable) > 0):
            return "True"
    return "False"

@register.filter
def Lastcheck(device_id):
    lable =  Importfile.objects.filter(lable=device_id , i_type=2)
    if (lable is not None):
        if (len(lable) > 0):
            return "True"
    return "False"    