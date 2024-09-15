from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# 在创建api的UI页面
# @api_view(['GET'])的意思是：只有GET请求才可以访问此controller
@api_view(['GET'])
def getRoute(request):
    # 列出来都有哪些api可以使用
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:roomId'
    ]
    return Response(routes)

# 查询所有room
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # 因为RESTFul api返回的是JSON对象，而rooms是Python对象
    # 因此需要使用serializer来将Python对象转化成JSON对象返回
    # 否则直接返回Python对象会报错！
    # many表示转化多个Python对象
    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer.data)

# 根据roomId查询room
@api_view(['GET'])
def getRoomByRoomId(request, roomId):
    room = Room.objects.get(id = roomId)
    # 因为RESTFul api返回的是JSON对象，而rooms是Python对象
    # 因此需要使用serializer来将Python对象转化成JSON对象返回
    # 否则直接返回Python对象会报错！
    serializer = RoomSerializer(room, many=False)

    return Response(serializer.data)