from django.contrib import admin
from  .models import *

class DeptAdmin(admin.ModelAdmin):
    list_display = ('dept_id','dept_parent', 'deptname','manager')
    search_fields = ('deptname','manager')
admin.site.register(Dept,DeptAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_id','typename')
    search_fields = ('type_id', 'typename')
admin.site.register(Type,TypeAdmin)

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_id', 'materialname','type_id')
    search_fields = ('material_id', 'materialname')
    def related_type(self, obj):
        return obj.type_id.typename
        related_material.short_description = 'typename'
admin.site.register(Material,MaterialAdmin)

class ItdeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'material_id','dept_id','user_name')
    search_fields = ('device_id', 'material_id__materialname','dept_id__deptname','user_name')

    def related_material(self, obj):
        return obj.material_id.materialname
        related_material.short_description = 'Materialname'

admin.site.register(Itdevice,ItdeviceAdmin)

