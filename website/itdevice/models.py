# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


class AuditlogLogentry(models.Model):
    object_pk = models.CharField(max_length=255)
    object_id = models.BigIntegerField(blank=True, null=True)
    object_repr = models.TextField()
    action = models.ForeignKey('UserAction', models.DO_NOTHING, db_column='action')
    changes = models.TextField()
    timestamp = models.DateTimeField()
    actor = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    remote_addr = models.CharField(max_length=39, blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditlog_logentry'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Dept(models.Model):
    dept_id = models.CharField(primary_key=True, max_length=5)
    dept_parent = models.CharField(max_length=5, blank=True, null=True)
    deptname = models.CharField(max_length=45)
    manager = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dept'
auditlog.register(Dept)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Importfile(models.Model):
    import_id = models.AutoField(primary_key=True)
    i = models.ForeignKey('Inventory', models.DO_NOTHING)
    i_type = models.ForeignKey('InventoryType', models.DO_NOTHING)
    lable = models.CharField(max_length=45)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'importfile'


class Inventory(models.Model):
    i_id = models.AutoField(primary_key=True)
    i_name_cn = models.CharField(max_length=100)
    i_name_vn = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'inventory'


class InventoryType(models.Model):
    i_type_id = models.AutoField(primary_key=True)
    i_type_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'inventory_type'


class Itdevice(models.Model):
    device_id = models.CharField(primary_key=True, max_length=45)
    material = models.ForeignKey('Material', models.DO_NOTHING)
    dept = models.ForeignKey(Dept, models.DO_NOTHING)
    pur_date = models.DateField()
    user_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itdevice'
auditlog.register(Itdevice)

class Material(models.Model):
    material_id = models.CharField(primary_key=True, max_length=45)
    materialname = models.CharField(max_length=200, blank=True, null=True)
    type = models.ForeignKey('Type', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material'


class Type(models.Model):
    type_id = models.CharField(primary_key=True, max_length=5)
    typename = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'type'
auditlog.register(Type)

class UserAction(models.Model):
    action_id = models.SmallIntegerField(primary_key=True)
    action_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user_action'
