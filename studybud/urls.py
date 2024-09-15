from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # 所有访问根路由的用户，都会去base app的url中进行匹配
    path('', include('base.urls')),
    # 如果url前缀是api，则匹配下面的route
    path('api/', include('base.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
