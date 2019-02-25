# _*_ coding: utf-8 _*_
# @time     : 2018/12/12
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from . import models
from users.serializers import RoleSerializers, UserProfileSerializers
from order.baseview import make_order_num


class NodeSreializer(serializers.ModelSerializer):
    """节点"""

    class Meta:
        model = models.Node
        fields = '__all__'


class NodeDetailSerializer(NodeSreializer):
    """节点详情"""
    role = RoleSerializers(read_only=True, many=True)


class ProcessSerializer(serializers.ModelSerializer):
    """审批连"""

    class Meta:
        model = models.Process
        fields = '__all__'

    def validate(self, attrs):
        if not isinstance(eval(attrs['flow']), list):
            return serializers.ValidationError('flow must like a "[1,2,3]" list type string.')
        return attrs


class ProcessDetailSerializer(ProcessSerializer):
    """审批链详情"""
    flow = serializers.SerializerMethodField(read_only=True)

    def get_flow(self, obj):
        ls = []
        flows = []
        try:
            print('---obj.flow:', obj.flow)
            flows = eval(obj.flow)
            print('--flows:', flows)
        except:
            pass
        count = 0
        for node in flows:
            node_obj = models.Node.objects.filter(id=node).first()
            json = NodeSreializer(node_obj).data
            json['count'] = count
            count += 1
            ls.append(json)
        return ls


class ApplySerializer(serializers.ModelSerializer):
    """审批表"""
    num = serializers.CharField(read_only=True)

    class Meta:
        model = models.Apply
        fields = '__all__'

    def create(self, validated_data):
        validated_data['num'] = make_order_num(model=self.Meta.model, start='AP')
        return super().create(validated_data)


class NodeStatusSerializer(serializers.ModelSerializer):
    """节点状态"""
    node_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.NodeStatus
        fields = '__all__'

    def get_node_name(self, obj):
        node_obj = models.Node.objects.filter(id=obj.node_id).first()
        name = node_obj.node if node_obj else '未知'
        return name


class NodeStatusDetailSerializer(NodeStatusSerializer):
    """节点状态详情"""
    apply = ApplySerializer(read_only=True, many=False)
    node = NodeSreializer(read_only=True, many=False)
    user = UserProfileSerializers(read_only=True, many=False)


class ApplyDetailSerializer(serializers.ModelSerializer):
    """审批表详情"""
    create_user = UserProfileSerializers(read_only=True, many=False)
    nodes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Apply
        fields = '__all__'

    def get_nodes(self, obj):
        nodes = []
        # 拿到节点状态表中的记录
        node_objs = models.NodeStatus.objects.filter(apply_id=obj.id)
        # 序列化， 排序返回
        for node_obj in node_objs:
            node_json = {}
            node_json = NodeStatusSerializer(node_obj).data
            nodes.append(node_json)
        ordering_nodes = self.ordering(nodes, obj)
        return ordering_nodes if ordering_nodes else '暂无'

    def ordering(self, nodes, obj):
        ordering_nodes = []
        type = self.obtain_type_by_target(obj.target)
        process_id = models.TypeProcess.objects.filter(target_type=type).first().process_id
        flow = eval(models.Process.objects.filter(id=process_id).first().flow)
        count = 0
        # 排序,确定rank后返回
        for node in flow:
            for n in nodes:
                if n['node'] == node:
                    n['rank'] = count
                    ordering_nodes.append(n)
            count += 1
        return ordering_nodes

    def obtain_type_by_target(self, target):
        import re
        if re.match(r'^W[0-9]+$', target):
            return 'warehouse'
        elif re.match(r'^B[0-9]+$', target):
            return 'box'
        elif re.match(r'^DQ[0-9]+$', target):
            return 'store_group'
        elif re.match(r'^DH[0-9]+$', target):
            return 'diaohuo'
        elif re.match(r'^TH[0-9]+$', target):
            return 'return'
        elif re.match(r'^CG[0-9]+$', target):
            return 'purchase'
        elif re.match(r'^CX[0-9]+$', target):
            return 'cuxiao'
        elif re.match(r'^BC[0-9]+$', target):
            return 'bucha'


class TypeProcessSerializer(serializers.ModelSerializer):
    """目标类型和流程关系"""

    class Meta:
        model = models.TypeProcess
        fields = '__all__'


class TypeProcessDetailSerializer(TypeProcessSerializer):
    process = ProcessSerializer(read_only=True, many=False)


if __name__ == '__main__':
    pass

