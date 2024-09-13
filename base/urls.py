from django.urls import path
from . import views

# 这里必须叫urlpatterns
urlpatterns = [
    # 注意！根路由不能写'/'，否则会出错！
    # name的值是在template中使用的使用使用的alias；如果name的值不变，但我们下面的path的第一个参数的字符串变了，也不会影响，因为我们在templates中使用的是name中的值；
    # 查询所有room的route
    path('', views.home, name='home'),
    # 根据id查询room的route
    path('room/<str:roomId>/', views.room, name='room'),
    # 创建room的route
    path('create_room/', views.createRoom, name='createRoom'),
    # 更新room的route
    path('update_room/<str:roomId>', views.updateRoom, name='updateRoom'),
    # 删除room的route
    path('delete_room/<str:roomId>', views.deleteRoom, name='deleteRoom'),
    # login用户的route
    path('login/', views.loginUser, name='login'),
    # logout用户的route
    path('logout/', views.logoutUser, name='logout'),
    # register用户的route
    path('register/', views.registerUser, name='register'),

    # 删除message的route
    path('delete_message/<str:messageId>', views.deleteComment, name='deleteMessage'),

    # 查询user的route
    path('profile/<str:userId>', views.userProfile, name='userProfile'),
]
