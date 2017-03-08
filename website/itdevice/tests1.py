import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import os
import datetime
from collections import defaultdict
import datetime as dt   
import csv

mysql_cnxn = create_engine('mysql+mysqldb://root:kevin6102531@localhost:3306/fixed_asset?charset=utf8')

script_path = os.path.dirname(__file__)

def parse_date(td):
    resYear = float(td.days)/364.0                   # get the number of years including the the numbers after the dot
    resMonth = int((resYear - int(resYear))*364/30)  # get the number of months, by multiply the number after the dot by 364 and divide by 30.
    resYear = int(resYear)
    return str(resYear) + "Y" + str(resMonth) + "m"

# itdevice_sql = ('SELECT * FROM fixed_asset.itdevice')
# df_itdevice = pd.read_sql(itdevice_sql, mysql_cnxn) 
# df_itdevice.to_csv(script_path,  index = False, encoding='utf-8')
df_itdevice_new_id_list = []
with open('itdevice.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print row[0]
		df_itdevice_new_id_list.append(row[0])
print df_itdevice_new_id_list
# df_itdevice_new_id_list = pd.read_csv('itdevice.csv')
# df_poh.to_sql('poh', mysql_cnxn, schema = 'nos', if_exists='replace', index=False )
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
df_itdevice_old_id_list = df_itdevice['device_id'].tolist()
df_itdevice = df_itdevice.merge(df_material, how='left', on=['material_id']).merge(df_type, how='left', on=['type_id']).merge(df_manager, how='left', on=['dept_id'])
df_itdevice['pur_date'] = df_itdevice['pur_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
df_itdevice['today_date'] = datetime.datetime.today().strftime("%Y-%m-%d")
df_itdevice['delta'] = [parse_date(datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.datetime.strptime(end, '%Y-%m-%d')) for start, end in zip(df_itdevice['today_date'], df_itdevice['pur_date'])]
# not_match_list = list(set(df_itdevice_old_id_list) - set(df_itdevice_new_id_list))
df_itdevice['first_review'] = ""
df_itdevice['second_review'] = ""
df_itdevice['sign'] = ''
df_itdevice = df_itdevice.reset_index(drop=True)
df_itdevice['id'] = df_itdevice.index +1
df_itdevice = df_itdevice[['id','user_name','typename','device_id','materialname','dept_id','manager','first_review','second_review','sign','delta']]

scan_dept_list = list(set(df_itdevice[df_itdevice.device_id.isin(df_itdevice_new_id_list)]['dept_id'].astype(str).tolist()))
total_device_scan_dept = len(df_itdevice[df_itdevice.dept_id.isin(scan_dept_list)])
print scan_dept_list
print total_device_scan_dept