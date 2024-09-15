from django.urls import path
from . import views

urlpatterns = [
    # 列出所有api route
    path('', views.getRoute),
    # 查询所有room的route
    path('rooms/', views.getRooms),
    # 根据roomId查询room的route
    path('rooms/<str:roomId>', views.getRoomByRoomId)
]
