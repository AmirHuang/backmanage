# Generated by Django 2.0.7 on 2018-12-12 15:18

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='电话')),
                ('superior', models.CharField(help_text='上级', max_length=20, null=True, verbose_name='上级')),
                ('address', models.CharField(max_length=100, null=True, verbose_name='地址')),
            ],
            options={
                'verbose_name': '用户账号',
                'verbose_name_plural': '用户账号',
                'db_table': 'userprofile',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('where', models.CharField(max_length=100, verbose_name='区域')),
            ],
            options={
                'verbose_name': '区域',
                'verbose_name_plural': '区域',
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='MemberProfile',
            fields=[
                ('num', models.CharField(help_text='会员编号', max_length=11, primary_key=True, serialize=False, verbose_name='会员编号')),
                ('phone', models.CharField(help_text='手机号', max_length=11, unique=True, verbose_name='手机号')),
                ('regist_source', models.CharField(help_text='注册来源', max_length=100, verbose_name='注册来源')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='注册时间', verbose_name='注册时间')),
                ('wechat_id', models.CharField(help_text='微信id', max_length=32, null=True, unique=True, verbose_name='微信id')),
                ('alipay_id', models.CharField(help_text='支付宝id', max_length=32, null=True, unique=True, verbose_name='支付宝id')),
                ('lianhua_id', models.CharField(help_text='联华会员id', max_length=32, null=True, unique=True, verbose_name='联华会员id')),
                ('lianhua_card', models.CharField(help_text='联华会员卡号', max_length=32, null=True, unique=True, verbose_name='联华会员卡号')),
                ('user_name', models.CharField(help_text='姓名', max_length=32, null=True, verbose_name='姓名')),
                ('idcard', models.CharField(help_text='身份证', max_length=18, null=True, unique=True, verbose_name='身份证')),
                ('photo', models.ImageField(help_text='人像', null=True, unique=True, upload_to='member/', verbose_name='人像')),
                ('fingerprint', models.CharField(help_text='指纹', max_length=255, null=True, unique=True, verbose_name='指纹')),
                ('rank', models.IntegerField(default=0, help_text='会员等级', verbose_name='会员等级')),
                ('points', models.IntegerField(default=0, help_text='会员积分', verbose_name='会员积分')),
                ('money', models.FloatField(default=0, help_text='余额', verbose_name='余额')),
            ],
            options={
                'verbose_name': '会员表',
                'verbose_name_plural': '会员表',
                'db_table': 'memberprofile',
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(max_length=100, unique=True, verbose_name='权限')),
                ('permission_remake', models.CharField(max_length=100, verbose_name='权限备注')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(max_length=100, unique=True, verbose_name='角色种类')),
                ('role_remake', models.CharField(max_length=100, null=True, verbose_name='角色备注')),
                ('permission', models.ManyToManyField(blank=True, to='users.Permissions', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'role',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Aera', verbose_name='所属区域'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ManyToManyField(blank=True, to='users.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
