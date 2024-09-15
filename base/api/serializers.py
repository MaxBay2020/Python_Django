# 此文件是用来将Python对象转化成JSON对象的
from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

