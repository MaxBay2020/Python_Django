from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

# 使用下面的方式帮助我们创建room表格的UI；
class RoomForm(ModelForm):
    class Meta:
        model = Room
        # __all__表示，room的form会在template中显示Room表中的所有字段
        # 如果不想全部显示在form表格中，则写成：
        # fields = ['name', 'description']
        fields = '__all__'
        # 在form表格中，不显示host和participants字段
        exclude = ['host', 'participants']

# 使用下面的方式帮助我们创建room表格的UI；
class UserForm(ModelForm):
    class Meta:
        model = User
        # 如果不想全部显示在form表格中，则写成：
        fields = ['username', 'email']

