from django.forms import ModelForm
# 使用自定义的User
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['username', 'email', 'name', 'avatar', 'bio']

# 用下面的方式创建自定义的注册用户的form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # 如果不想全部显示在form表格中，则写成：
        fields = ['email', 'password1', 'password2', 'avatar']