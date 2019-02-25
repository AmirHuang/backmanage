# Generated by Django 2.0.7 on 2018-12-13 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operatorsystem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0, help_text='库存数量', verbose_name='库存数量')),
                ('price', models.FloatField(blank=True, help_text='售价', null=True, verbose_name='售价')),
                ('box', models.ForeignKey(help_text='门店', on_delete=django.db.models.deletion.CASCADE, to='operatorsystem.BoxManage', verbose_name='门店')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '门店库存信息',
                'verbose_name_plural': '门店库存信息',
                'db_table': 'box_inventory',
            },
        ),
        migrations.CreateModel(
            name='BuCha2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(help_text='销售数量', verbose_name='销售数量')),
                ('bcprice', models.FloatField(help_text='补差金额', verbose_name='补差金额')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_bc', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '补差商品',
                'verbose_name_plural': '补差商品',
                'db_table': 'bucha2goods',
            },
        ),
        migrations.CreateModel(
            name='BuChaOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='单号', max_length=14, null=True, verbose_name='单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('input_time', models.DateTimeField(help_text='进货时间', verbose_name='进货时间')),
                ('remark', models.CharField(help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '审核中'), (1, '已通过'), (2, '不通过'), (3, '已关闭'), (4, '待结算'), (5, '已结算')], default=0, help_text='审核状态', verbose_name='审核状态')),
            ],
            options={
                'verbose_name': '补差单',
                'verbose_name_plural': '补差单',
                'db_table': 'bucha_order',
            },
        ),
        migrations.CreateModel(
            name='ChuKuOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('num', models.CharField(help_text='退货出库单号', max_length=14, null=True, unique=True, verbose_name='退货出库单号')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('related_order', models.CharField(help_text='对应退货单', max_length=30, verbose_name='对应退货单')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '待分拣'), (1, '待出库'), (2, '在途'), (3, '完成')], default=0)),
                ('officer', models.ForeignKey(help_text='负责人', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='r_order', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
            ],
            options={
                'verbose_name': '出库单',
                'verbose_name_plural': '出库单',
                'db_table': 'chuku_order',
            },
        ),
        migrations.CreateModel(
            name='CuXiao2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('except_tax_cg_price', models.FloatField(help_text='不含税进价', verbose_name='不含税进价')),
                ('include_tax_cg_price', models.FloatField(help_text='含税进价', verbose_name='含税进价')),
                ('except_tax_sl_price', models.FloatField(help_text='不含税售价', verbose_name='不含税售价')),
                ('include_tax_sl_price', models.FloatField(help_text='含税售价', verbose_name='含税售价')),
                ('profit', models.FloatField(help_text='毛利额', verbose_name='毛利额')),
                ('profit_rate', models.FloatField(help_text='毛利率', verbose_name='毛利率')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_cx', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '促销商品中间表',
                'verbose_name_plural': '促销商品中间表',
                'db_table': 'cuxiao2goods',
            },
        ),
        migrations.CreateModel(
            name='CuXiaoOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='单号', max_length=14, null=True, verbose_name='单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('start_time', models.DateTimeField(help_text='促销开始时间', null=True, verbose_name='促销开始时间')),
                ('end_time', models.DateTimeField(help_text='促销结束时间', verbose_name='促销结束时间')),
                ('scheme', models.IntegerField(choices=[(0, '前台让利'), (1, '后台补差')], default=1, help_text='促销形式', verbose_name='促销形式')),
                ('remark', models.CharField(help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '审核中'), (1, '已通过'), (2, '不通过'), (3, '已关闭')], default=0, help_text='审核状态', verbose_name='审核状态')),
                ('box', models.ManyToManyField(help_text='门店', to='operatorsystem.BoxManage', verbose_name='门店')),
                ('create_user', models.ForeignKey(help_text='发起人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='发起人')),
                ('goods', models.ManyToManyField(help_text='商品', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '促销单',
                'verbose_name_plural': '促销单',
                'db_table': 'cuxiao_order',
            },
        ),
        migrations.CreateModel(
            name='DiaoHuo2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=1, help_text='数量', verbose_name='数量')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_dh', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '调货单商品表',
                'verbose_name_plural': '调货单商品表',
                'db_table': 'diaohuo2goods',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DiaoHuoOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='单号', max_length=14, null=True, unique=True, verbose_name='单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('expire_time', models.DateTimeField(help_text='有效时间', null=True, verbose_name='有效时间')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('type', models.IntegerField(choices=[(0, '店到店'), (1, '店到仓'), (2, '仓到仓'), (3, '仓到店')], default=2, help_text='调拨方式', verbose_name='调拨方式')),
                ('from_id', models.IntegerField(help_text='出库点', verbose_name='出库点')),
                ('to_id', models.IntegerField(help_text='入库点', verbose_name='入库点')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=200, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '审核中'), (1, '已通过'), (2, '不通过'), (3, '已关闭'), (4, '待出库'), (5, '待入库'), (6, '部分完成'), (7, '已完成')], default=0, help_text='审核状态', verbose_name='审核状态')),
                ('create_user', models.ForeignKey(help_text='发起人', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dh_orders', to=settings.AUTH_USER_MODEL, verbose_name='发起人')),
                ('goods', models.ManyToManyField(through='order.DiaoHuo2Goods', to='operatorsystem.GoodsManage')),
            ],
            options={
                'verbose_name': '调货单',
                'verbose_name_plural': '调货单',
                'db_table': 'diaohuo_order',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Order2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(verbose_name='交易商品数量')),
                ('goods', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_cg', to='operatorsystem.GoodsManage', verbose_name='商品id')),
            ],
            options={
                'verbose_name': '采购单商品中间表',
                'verbose_name_plural': '采购单商品中间表',
                'db_table': 'order2goods',
            },
        ),
        migrations.CreateModel(
            name='PanDian2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(help_text='盘点数量', verbose_name='盘点数量')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_pd', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '盘点单商品中间表',
                'verbose_name_plural': '盘点单商品中间表',
                'db_table': 'pandian2goods',
            },
        ),
        migrations.CreateModel(
            name='PanDianOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='盘点单号', max_length=32, null=True, unique=True, verbose_name='盘点单号')),
                ('target', models.IntegerField(help_text='盘点目标', verbose_name='盘点目标')),
                ('type', models.IntegerField(choices=[(0, '仓库'), (1, '门店')], help_text='盘点对象类型', verbose_name='盘点对象类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=200, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '审批中'), (1, '已通过'), (2, '不通过'), (3, '已关闭')], default=0, help_text='状态', verbose_name='状态')),
                ('goods', models.ManyToManyField(help_text='商品', through='order.PanDian2Goods', to='operatorsystem.GoodsManage', verbose_name='商品')),
                ('pduser', models.ForeignKey(help_text='盘点人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='盘点人')),
            ],
            options={
                'verbose_name': '盘点单',
                'verbose_name_plural': '盘点单',
                'db_table': 'pandian_order',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(auto_created=True, default=order.models.three_days_next, help_text='有效时间', verbose_name='有效时间')),
                ('create_time', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='采购单创建时间')),
                ('num', models.CharField(max_length=14, unique=True, verbose_name='采购单号')),
                ('finish_time', models.DateTimeField(blank=True, help_text='实际完成时间', null=True, verbose_name='实际完成时间')),
                ('recv_id', models.IntegerField(help_text='入库点id', verbose_name='入库点id')),
                ('recv_type', models.IntegerField(choices=[(0, '仓库'), (1, '门店')], default=0, help_text='入库类型', verbose_name='入库类型')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '审核中'), (1, '已通过'), (2, '不通过'), (3, '已关闭'), (4, '已发货'), (5, '部分完成'), (6, '已完成')], default=0, help_text='审核状态', verbose_name='审核状态')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='采购单发起人')),
                ('goods', models.ManyToManyField(through='order.Order2Goods', to='operatorsystem.GoodsManage', verbose_name='货物')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.Supplier', verbose_name='供应商')),
            ],
            options={
                'verbose_name': '采购单',
                'verbose_name_plural': '采购单',
                'db_table': 'purchase_order',
            },
        ),
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(auto_created=True, default=order.models.three_days_next, help_text='有效时间', verbose_name='有效时间')),
                ('create_time', models.DateTimeField(auto_created=True, auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('send_id', models.IntegerField(help_text='出库点id', verbose_name='出库点id')),
                ('send_type', models.IntegerField(choices=[(0, '仓库'), (1, '门店')], default=0, help_text='出库类型', verbose_name='出库类型')),
                ('num', models.CharField(help_text='退货单号', max_length=14, null=True, unique=True, verbose_name='退货单号')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('status', models.IntegerField(choices=[(0, '审核中'), (1, '已通过'), (2, '不通过'), (3, '已关闭'), (4, '已发货'), (5, '部分完成'), (6, '已完成')], default=0, help_text='审核状态', verbose_name='审核状态')),
                ('create_user', models.ForeignKey(blank=True, help_text='创建者', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '退货单',
                'verbose_name_plural': '退货单',
                'db_table': 'return_order',
            },
        ),
        migrations.CreateModel(
            name='ReturnOrder2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(help_text='退货数量', verbose_name='退货数量')),
                ('remark', models.CharField(default='', help_text='退货备注', max_length=30, verbose_name='退货备注')),
                ('goods', models.ForeignKey(blank=True, help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_rt', to='operatorsystem.GoodsManage', verbose_name='商品')),
                ('order', models.ForeignKey(blank=True, help_text='退货单', null=True, on_delete=django.db.models.deletion.CASCADE, to='order.ReturnOrder', verbose_name='退货单')),
                ('source', models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单')),
            ],
            options={
                'verbose_name': '退货商品中间表',
                'verbose_name_plural': '退货商品中间表',
                'db_table': 'returnorder2goods',
            },
        ),
        migrations.CreateModel(
            name='RuKuOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('related_order', models.CharField(help_text='对应单据', max_length=30, verbose_name='对应单据')),
                ('num', models.CharField(help_text='入库单号', max_length=14, null=True, unique=True, verbose_name='入库单号')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=100, null=True, verbose_name='备注')),
                ('status', models.IntegerField(choices=[(0, '待出库'), (1, '在途'), (2, '部分完成'), (3, '已完成')], default=0)),
                ('officer', models.ForeignKey(help_text='负责人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
            ],
            options={
                'verbose_name': '入库单',
                'verbose_name_plural': '入库单',
                'db_table': 'ruku_order',
            },
        ),
        migrations.CreateModel(
            name='Sale2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(help_text='商品数量', verbose_name='商品数量')),
                ('is_discount', models.BooleanField(default=False, help_text='促销标记', verbose_name='促销标记')),
                ('include_tax_cg_price', models.FloatField(help_text='含税进价', verbose_name='含税进价')),
                ('include_tax_sl_price', models.FloatField(help_text='含税售价', verbose_name='含税售价')),
                ('except_tax_cg_price', models.FloatField(help_text='不含税进价', verbose_name='不含税进价')),
                ('except_tax_sl_price', models.FloatField(help_text='不含税售价', verbose_name='不含税售价')),
                ('profit', models.FloatField(help_text='毛利额', verbose_name='毛利额')),
                ('profit_rate', models.FloatField(help_text='毛利率', verbose_name='毛利率')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_sl', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '销售单商品表',
                'verbose_name_plural': '销售单商品表',
                'db_table': 'sale2goods',
            },
        ),
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='单号', max_length=16, null=True, unique=True, verbose_name='单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('money', models.FloatField(help_text='支付金额', verbose_name='支付金额')),
                ('payments', models.CharField(help_text='支付方式', max_length=20, verbose_name='支付方式')),
                ('pay_time', models.DateTimeField(auto_now_add=True, help_text='支付时间', verbose_name='支付时间')),
                ('finish_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('status', models.IntegerField(choices=[(0, '已完成'), (1, '已失效'), (2, '已退货'), (3, '部分退货')], default=0, help_text='状态', verbose_name='状态')),
                ('box', models.ForeignKey(help_text='门店', null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.BoxManage', verbose_name='门店')),
                ('goods', models.ManyToManyField(help_text='订单中的商品', through='order.Sale2Goods', to='operatorsystem.GoodsManage', verbose_name='订单中的商品')),
                ('member', models.ForeignKey(help_text='会员', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.MemberProfile', verbose_name='会员')),
            ],
            options={
                'verbose_name': '销售单',
                'verbose_name_plural': '销售单',
                'db_table': 'sale_order',
            },
        ),
        migrations.CreateModel(
            name='SunYi2Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ex_num', models.IntegerField(help_text='差异数量', verbose_name='差异数量')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goods_in_sy', to='operatorsystem.GoodsManage', verbose_name='商品')),
            ],
            options={
                'verbose_name': '损益商品中间表',
                'verbose_name_plural': '损益商品中间表',
                'db_table': 'sunyi2goods',
            },
        ),
        migrations.CreateModel(
            name='SunYiOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(help_text='损益单号', max_length=32, null=True, unique=True, verbose_name='损益单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('goods', models.ManyToManyField(through='order.SunYi2Goods', to='operatorsystem.GoodsManage')),
                ('pdorder', models.ForeignKey(help_text='盘点单', on_delete=django.db.models.deletion.CASCADE, to='order.PanDianOrder', verbose_name='盘点单')),
            ],
            options={
                'verbose_name': '损益单',
                'verbose_name_plural': '损益单',
                'db_table': 'sunyi_order',
            },
        ),
        migrations.CreateModel(
            name='WareHouseInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0, help_text='库存数量', verbose_name='库存数量')),
                ('goods', models.ForeignKey(help_text='商品', null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.GoodsManage', verbose_name='商品')),
                ('source', models.ForeignKey(help_text='来源单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源单')),
                ('ware_house', models.ForeignKey(help_text='仓库', on_delete=django.db.models.deletion.CASCADE, to='operatorsystem.WareHouse', verbose_name='仓库')),
            ],
            options={
                'verbose_name': '仓库库存信息',
                'verbose_name_plural': '仓库库存信息',
                'db_table': 'warehouse_inventory',
            },
        ),
        migrations.AddField(
            model_name='sunyi2goods',
            name='order',
            field=models.ForeignKey(help_text='损益单', on_delete=django.db.models.deletion.CASCADE, to='order.SunYiOrder', verbose_name='损益单'),
        ),
        migrations.AddField(
            model_name='sunyi2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='sale2goods',
            name='order',
            field=models.ForeignKey(help_text='销售单', on_delete=django.db.models.deletion.CASCADE, to='order.SaleOrder', verbose_name='销售单'),
        ),
        migrations.AddField(
            model_name='sale2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='returnorder',
            name='goods',
            field=models.ManyToManyField(help_text='商品', through='order.ReturnOrder2Goods', to='operatorsystem.GoodsManage', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='returnorder',
            name='supplier',
            field=models.ForeignKey(blank=True, help_text='供应商', null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.Supplier', verbose_name='供应商'),
        ),
        migrations.AddField(
            model_name='pandian2goods',
            name='order',
            field=models.ForeignKey(help_text='盘点单', on_delete=django.db.models.deletion.CASCADE, to='order.PanDianOrder', verbose_name='盘点单'),
        ),
        migrations.AddField(
            model_name='pandian2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='order2goods',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.PurchaseOrder', verbose_name='采购单id'),
        ),
        migrations.AddField(
            model_name='diaohuo2goods',
            name='order',
            field=models.ForeignKey(help_text='所属订单', on_delete=django.db.models.deletion.CASCADE, to='order.DiaoHuoOrder', verbose_name='所属订单'),
        ),
        migrations.AddField(
            model_name='diaohuo2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='cuxiao2goods',
            name='order',
            field=models.ForeignKey(help_text='促销单', on_delete=django.db.models.deletion.CASCADE, to='order.CuXiaoOrder', verbose_name='促销单'),
        ),
        migrations.AddField(
            model_name='cuxiao2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='buchaorder',
            name='cxorder',
            field=models.ForeignKey(help_text='促销单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.CuXiaoOrder', verbose_name='促销单'),
        ),
        migrations.AddField(
            model_name='buchaorder',
            name='goods',
            field=models.ManyToManyField(through='order.BuCha2Goods', to='operatorsystem.GoodsManage'),
        ),
        migrations.AddField(
            model_name='buchaorder',
            name='supplier',
            field=models.ForeignKey(help_text='供应商', null=True, on_delete=django.db.models.deletion.SET_NULL, to='operatorsystem.Supplier', verbose_name='供应商'),
        ),
        migrations.AddField(
            model_name='bucha2goods',
            name='order',
            field=models.ForeignKey(help_text='补差单', on_delete=django.db.models.deletion.CASCADE, to='order.BuChaOrder', verbose_name='补差单'),
        ),
        migrations.AddField(
            model_name='bucha2goods',
            name='source',
            field=models.ForeignKey(help_text='来源采购单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源采购单'),
        ),
        migrations.AddField(
            model_name='boxinventory',
            name='source',
            field=models.ForeignKey(help_text='来源单', null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.PurchaseOrder', to_field='num', verbose_name='来源单'),
        ),
        migrations.AlterUniqueTogether(
            name='sale2goods',
            unique_together={('order', 'goods', 'source')},
        ),
        migrations.AlterUniqueTogether(
            name='order2goods',
            unique_together={('goods', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='diaohuo2goods',
            unique_together={('order', 'goods', 'source')},
        ),
    ]
