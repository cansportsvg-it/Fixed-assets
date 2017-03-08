from  django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from models import *

class ItdeviceForm(forms.ModelForm):
    class Meta:
        model = Itdevice
        fields = ('device_id', 'material', 'dept', 'pur_date', 'user_name')
    def clean_device_id(self):
        device_id = self.cleaned_data['device_id']
        if Itdevice.objects.filter(device_id=device_id).exists():
            raise ValidationError("Device already exists")
        return device_id      

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('type_id', 'typename',)
    def clean_type_id(self):
        type_id = self.cleaned_data['type_id']
        if Type.objects.filter(type_id=type_id).exists():
            raise ValidationError("Type already exists")
        return type_id    
    def clean_typename(self):
        typename = self.cleaned_data['typename']
        return typename     

class DeptForm(forms.ModelForm):
    class Meta:
        model = Dept
        fields = ('dept_id', 'dept_parent','deptname', 'manager')
    def clean_dept_id(self):
        dept_id = self.cleaned_data['dept_id']
        if Dept.objects.filter(dept_id=dept_id).exists():
            raise ValidationError("Dept already exists")
        return dept_id     

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material_id', 'materialname', 'type')
    def clean_Material_id(self):
        material_id = self.cleaned_data['material_id']
        if Material.objects.filter(material_id=material_id).exists():
            raise ValidationError("Material already exists")
        return material_id    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class ImportForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Importfile
        fields = ['i','i_type','lable','date']
