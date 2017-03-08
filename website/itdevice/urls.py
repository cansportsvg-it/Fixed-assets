from django.conf.urls import url
#from .models import Dept
# Create your tests here.
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),

    url(r'^adddevice/$', views.add_itdevice, name='add_device'),
    url(r'^addmaterial/$', views.add_material, name='add_material'),
    url(r'^adddept/$', views.add_dept, name='add_dept'),
    url(r'^addtype/$', views.add_type, name='add_type'),

    url(r'^editdevice/(?P<device_id>[\w]+)/$', views.edit_device, name='edit_device'),
    url(r'^editmaterial/(?P<material_id>[\w]+)/$', views.edit_material, name='edit_material'),
    url(r'^editdept/(?P<dept_id>[\w]+)/$', views.edit_dept, name='edit_dept'),
    url(r'^edittype/(?P<type_id>[\w]+)/$', views.edit_type, name='edit_type'),

    url(r'^deletedevice/(?P<device_id>[\w]+)/$', views.delete_device, name='delete_device'),
    url(r'^deletematerial/(?P<material_id>[\w]+)/$', views.delete_material, name='delete_material'),
    url(r'^deletedept/(?P<dept_id>[\w]+)/$', views.delete_dept, name='delete_dept'),
    url(r'^deletetype/(?P<type_id>[\w]+)/$', views.delete_type, name='delete_type'),

    url(r'^dept/(?P<dept_id>[\w]+)/$', views.dept_filter, name='dept filter'),
    url(r'^date/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$', views.date_filter, name='dept filter'),
    url(r'^log/$', views.log, name='log'),
    url(r'^import/$', views.import_file, name='import'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^asset_cal/$', views.asset_cal, name='asset_cal'),
]