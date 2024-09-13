from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 所有访问根路由的用户，都会去base app的url中进行匹配
    path('', include('base.urls'))
]
