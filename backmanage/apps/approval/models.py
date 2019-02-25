from django.db import models
from users.models import Role, UserProfile


# Create your models here.


class Node(models.Model):
    """审批节点表"""
    node = models.CharField(max_length=32, null=False, verbose_name='节点名称', help_text='节点名称', unique=True)
    role = models.ManyToManyField(to=Role, verbose_name='审批所需角色', help_text='审批所需角色')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', help_text='创建时间')
    remark = models.CharField(null=True, max_length=32, verbose_name='备注', help_text='备注')

    class Meta:
        verbose_name_plural = verbose_name = '审批节点表'
        db_table = 'node'

    def __str__(self):
        return self.node


class Process(models.Model):
    """审批流程表"""
    process = models.CharField(max_length=32, null=False, verbose_name='流程名', help_text='流程名', unique=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间', help_text='创建时间')
    remark = models.CharField(max_length=32, null=True, verbose_name='备注', help_text='备注')
    flow = models.CharField(max_length=100, null=False, verbose_name='审批链条', help_text='审批链条')

    class Meta:
        verbose_name_plural = verbose_name = '审批流程'
        db_table = 'process'

    def __str__(self):
        return self.process


class TypeProcess(models.Model):
    """目标类型和流程关系表"""
    target_type = models.CharField(max_length=32, null=False, unique=True, verbose_name='目标类型', help_text='目标类型')
    process = models.ForeignKey(to=Process, on_delete=models.CASCADE, verbose_name='流程', help_text='流程')
    remark = models.CharField(max_length=32, null=True, verbose_name='备注', help_text='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    modefied = models.DateTimeField(auto_now=True, verbose_name='上次修改', help_text='上次修改')

    class Meta:
        verbose_name_plural = verbose_name = '目标类型和流程关系'
        db_table = 'type_process'


class Apply(models.Model):
    """审批申请表"""
    types = (
        (0, '自动'),
        (1, '手动')
    )
    statuses = (
        (0, '审批中'),
        (1, '已通过'),
        (2, '不通过'),
        (3, '已关闭')
    )
    num = models.CharField(max_length=14, null=True, verbose_name='审批号', help_text='审批号', unique=True)
    desc = models.CharField(max_length=32, null=True, verbose_name='描述', help_text='描述')
    target = models.CharField(max_length=32, null=False, verbose_name='目标数据', help_text='目标数据')
    type = models.IntegerField(choices=types, default=0, null=False, verbose_name='发起类型', help_text='发起类型')
    create_user = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='发起人',
                                    help_text='发起人')
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='发起时间', help_text='发起时间')
    modefied = models.DateTimeField(auto_now=True, null=False, verbose_name='上次变更', help_text='上次变更')
    status = models.IntegerField(choices=statuses, default=0, null=False, verbose_name='审批状态', help_text='审批状态')

    class Meta:
        verbose_name_plural = verbose_name = '审批记录表'
        db_table = 'apply'

    def __str__(self):
        return self.num


class NodeStatus(models.Model):
    """审批数据节点状态表"""
    statuses = (
        ('toapproval', '待审批'),
        ('approvaling', '审批中'),
        ('passed', '已通过'),
        ('nopass', '不通过')
    )
    apply = models.ForeignKey(to=Apply, related_name='nodes', on_delete=models.CASCADE, verbose_name='审核记录',
                              help_text='审核记录')
    node = models.ForeignKey(to=Node, on_delete=models.SET_NULL, null=True, verbose_name='节点', help_text='节点')
    status = models.CharField(default='toapproval', max_length=32, null=False, verbose_name='节点状态', help_text='节点状态')
    user = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='操作人', help_text='操作人')
    modefied = models.DateTimeField(auto_now=True, null=False, verbose_name='变更时间', help_text='变更时间')

    class Meta:
        verbose_name_plural = verbose_name = '数据和节点状态'
        unique_together = (('apply', 'node'),)
        db_table = 'nodestatus'

    def __str__(self):
        return self.apply.desc, self.node.node
