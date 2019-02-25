# Generated by Django 2.0.7 on 2018-12-13 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='审批号', max_length=14, null=True, unique=True, verbose_name='审批号')),
                ('desc', models.CharField(help_text='描述', max_length=32, null=True, verbose_name='描述')),
                ('target', models.CharField(help_text='目标数据', max_length=32, verbose_name='目标数据')),
                ('type', models.IntegerField(choices=[(0, '自动'), (1, '手动')], default=0, help_text='发起类型', verbose_name='发起类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='发起时间', verbose_name='发起时间')),
                ('modefied', models.DateTimeField(auto_now=True, help_text='上次变更', verbose_name='上次变更')),
                ('status', models.IntegerField(choices=[(0, '审批中'), (1, '已通过'), (2, '不通过'), (3, '已关闭')], default=0, help_text='审批状态', verbose_name='审批状态')),
                ('create_user', models.ForeignKey(help_text='发起人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='发起人')),
            ],
            options={
                'verbose_name': '审批记录表',
                'verbose_name_plural': '审批记录表',
                'db_table': 'apply',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(help_text='节点名称', max_length=32, unique=True, verbose_name='节点名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('remark', models.CharField(help_text='备注', max_length=32, null=True, verbose_name='备注')),
                ('role', models.ManyToManyField(help_text='审批所需角色', to='users.Role', verbose_name='审批所需角色')),
            ],
            options={
                'verbose_name': '审批节点表',
                'verbose_name_plural': '审批节点表',
                'db_table': 'node',
            },
        ),
        migrations.CreateModel(
            name='NodeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='toapproval', help_text='节点状态', max_length=32, verbose_name='节点状态')),
                ('modefied', models.DateTimeField(auto_now=True, help_text='变更时间', verbose_name='变更时间')),
                ('apply', models.ForeignKey(help_text='审核记录', on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='approval.Apply', verbose_name='审核记录')),
                ('node', models.ForeignKey(help_text='节点', null=True, on_delete=django.db.models.deletion.SET_NULL, to='approval.Node', verbose_name='节点')),
                ('user', models.ForeignKey(help_text='操作人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
            ],
            options={
                'verbose_name': '数据和节点状态',
                'verbose_name_plural': '数据和节点状态',
                'db_table': 'nodestatus',
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(help_text='流程名', max_length=32, unique=True, verbose_name='流程名')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('remark', models.CharField(help_text='备注', max_length=32, null=True, verbose_name='备注')),
                ('flow', models.CharField(help_text='审批链条', max_length=100, verbose_name='审批链条')),
            ],
            options={
                'verbose_name': '审批流程',
                'verbose_name_plural': '审批流程',
                'db_table': 'process',
            },
        ),
        migrations.CreateModel(
            name='TypeProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_type', models.CharField(help_text='目标类型', max_length=32, unique=True, verbose_name='目标类型')),
                ('remark', models.CharField(help_text='备注', max_length=32, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('modefied', models.DateTimeField(auto_now=True, help_text='上次修改', verbose_name='上次修改')),
                ('process', models.ForeignKey(help_text='流程', on_delete=django.db.models.deletion.CASCADE, to='approval.Process', verbose_name='流程')),
            ],
            options={
                'verbose_name': '目标类型和流程关系',
                'verbose_name_plural': '目标类型和流程关系',
                'db_table': 'type_process',
            },
        ),
        migrations.AlterUniqueTogether(
            name='nodestatus',
            unique_together={('apply', 'node')},
        ),
    ]