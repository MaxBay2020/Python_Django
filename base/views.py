from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.http import HttpResponse

def home(request):
    # 如果访问此controller的请求是GET请求
    searchKeyword = request.GET.get('searchKeyword')

    # 获取全部rooms
    # filter()方法来进行查询
    # 注意！
    # topic__name=topic的意思是对room表的topic的值进行精准匹配；
    # topic__name__icontains的意思是，只要topic的name包含searchKeyword即可，不区分大小写
    # topic__name__contains的意思是，只要topic的name包含searchKeyword即可，区分大小写
    # 使用Q()方法来追加过滤条件；
    # 如果有searchKeyword就过滤，如果没有就查询所有；
    rooms = Room.objects.filter(
        Q(topic__name__icontains=searchKeyword) |
        Q(name__icontains=searchKeyword) |
        Q(description__icontains=searchKeyword)
    ) if searchKeyword != None else Room.objects.all()

    # 获取room的数量
    # 也可以使用rooms.len()，但是count()是query的方法，比len()方法快；
    room_count = rooms.count()

    # 获取全部topic
    topics = Topic.objects.all()

    # 查询所有message
    roomComments = Message.objects.filter(
        Q(room__topic__name__icontains = searchKeyword)
    ) if searchKeyword != None else Message.objects.all()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'roomComments': roomComments,
    }

    return render(request, 'base/home.html', context)

# 根据roomId查询room
def room(request, roomId):
    # 获取制定roomId的room
    room = Room.objects.get(id=int(roomId))

    # 查询该room中的所有message
    # 如果是多对一的关系，需要使用xxx_set.all()的方式，其表示查询xxx表的属于该room的所有xxx
    # order_by('-created')表示：按照created字段进行降序排列，如果是升序，则是order_by('created')
    comments = room.message_set.all().order_by('-created')

    # 查询所有participants
    # 如果是多对多的关系，就直接使用.all()方法即可
    participants = room.participants.all()
    print(participants)

    # 如果访问此controller的请求是POST请求：说明要添加comment
    if request.method == 'POST':
        # 添加comment
        comment = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('commentBody')
        )

        # 如果当前用户评论了，就将该用户就加到participants中
        room.participants.add(request.user)

        # 因为alias是room的route需要传一个动态参数roomId；因此需要指定第二个参数
        return redirect('room', roomId = room.id)

    context = {
        'room': room,
        'comments': comments,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

# 创建room
# 只用登录的用户才能访问此controller
# login_url='login'的意思是如果用户没有登录，则跳转到login对应的路由
@login_required(login_url='login')
def createRoom(request):
    # 使用RoomForm()方法来渲染room中的字段到UI中；
    roomForm = RoomForm()

    topics = Topic.objects.all()

    # 如果访问此controll的请求是POST请求
    if request.method == 'POST':
        # 从form中获取topic的值
        topicName = request.POST.get('topic')
        # 下面代码的意思是：
        # 如果Topic表中，存在topicName值，created的值就是False，topic就是该topicName；
        # 如果Topic表中，不存在topicName的值，create的值就是True，topic就是该topicName；
        topic, created = Topic.objects.get_or_create(name = topicName)

        # 创建room对象并存入到db中
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')



        # # body的信息放在了request.POST中；
        # # 我们不需要手动给每个field进行赋值；我们使用下面的方式自动对对应的字段进行赋值；
        # # 准备room数据
        # newRoom = RoomForm(request.POST)
        # # 对每个field进行有效性验证，如在models.py中的max_length=200
        # if newRoom.is_valid():
        #     # 存入数据库
        #     # 在存入db之前，需要指定当前room的主人
        #     currentRoom = newRoom.save(commit = False)
        #     currentRoom.host = request.user
        #     currentRoom.save()
        #     # redirect()中的参数也是urls.py文件中的每个route中的name的值
        #     # 创建完room后，跳转到home路由所对应的页面；
        #     return redirect('home')


    context = {
        'roomForm': roomForm,
        'topics': topics
    }
    return render(request, 'base/room_form.html', context)

# 根据roomId更新room
@login_required(login_url='login')
def updateRoom(request, roomId):
    # 先根据roomId查找room
    currentRoom = Room.objects.get(id=roomId)
    # 渲染旧的room数据
    roomForm = RoomForm(instance=currentRoom)

    topics = Topic.objects.all()

    # 如果登录的user不是该room的主人
    if request.user != currentRoom.host:
        return HttpResponse('You are not allowed to update this room!')

    # 如果访问此controll的请求是POST请求
    # 注意！这里应该是PUT请求，但我们不是开发RESTFul api；因为是update数据；但是我们的创建和更新共享了一个UI，即room_form.html，因此这里就是POST请求；
    if request.method == 'POST':

        # 从form中获取topic的值
        topicName = request.POST.get('topic')
        # 下面代码的意思是：
        # 如果Topic表中，存在topicName值，created的值就是False，topic就是该topicName；
        # 如果Topic表中，不存在topicName的值，create的值就是True，topic就是该topicName；
        topic, created = Topic.objects.get_or_create(name=topicName)
        currentRoom.name = request.POST.get('name')
        # 因为用户可能添加新的topic
        currentRoom.topic = topic
        currentRoom.description = request.POST.get('description')

        # 存入到db中
        currentRoom.save()
        return redirect('home')

        # # 我们不需要手动给每个field进行赋值；我们使用下面的方式自动对对应的字段进行赋值；
        # # 将旧的room数据替换成新的room数据
        # updatedRoom = RoomForm(request.POST, instance=currentRoom)
        # if updatedRoom.is_valid():
        #     updatedRoom.save()
        #     # 更新完room后，跳转到home路由所对应的页面；
        #     return redirect('home')

    context = {
        'roomForm': roomForm,
        'topics': topics,
        'room': currentRoom
    }

    return render(request, 'base/room_form.html', context)

# 根据roomId删除room
@login_required(login_url='login')
def deleteRoom(request, roomId):
    currentRoom = Room.objects.get(id=roomId)

    # 如果登录的user不是该room的主人
    if request.user != currentRoom.host:
        return HttpResponse('You are not allowed to update this room!')

    # 如果访问此controller的请求是POST请求，说明要删除room了
    if request.method == 'POST':
        # 删除该room
        currentRoom.delete()
        # 删除完room后，跳转到home路由所对应的页面；
        return redirect('home')

    return render(request, 'base/delete.html', { 'obj': currentRoom })


# 用户登陆
def loginUser(request):
    # 如果用户已经登陆了，则跳转到home对应的路由
    if request.user.is_authenticated:
        return redirect('home')

    # 如果访问此controller的请求是POST请求
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # 根据username查找用户
            user = User.objects.get(username = username)
        except:
            # 如果没找到该user，显示flash message
            messages.error(request, "User does not exist!")

        # 如果用户存在，则进行密码验证
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 如果用户通过验证
            login(request, user)
            return redirect('home')
        else:
            # 如果用户没通过验证
            messages.error(request, "Username or password does not exist!")

    # 因为login的controller和register的controller使用的是同一个页面，即login_register.html页面
    # 因此需要使用一个变量来进行区分，之后再login_register.html页面进行条件渲染
    currentPage = 'loginPage'
    context = {
        'currentPage': currentPage
    }
    return render(request, 'base/login_register.html', context)

# register用户
def registerUser(request):

    # 我们使用Django提供的register用户的form的UI
    registerUserForm = UserCreationForm()

    # 如果访问此controller的请求是POST请求
    if request.method == 'POST':
        # 准备数据
        registerUserForm = UserCreationForm(request.POST)
        if registerUserForm.is_valid():
            # 如果数据通过了验证，则保存到database中
            # commit=False的意思是先不要存到database中，做一些处理之后才存到db中；
            # 在这里是将username全部转化成小写之后再存入到db中；
            user = registerUserForm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # 用户register成功后，login该user，并跳到home对应的route；
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User is NOT valid')

    # 因为login的controller和register的controller使用的是同一个页面，即login_register.html页面
    # 因此需要使用一个变量来进行区分，之后再login_register.html页面进行条件渲染
    currentPage = 'registerPage'
    context = {
        'currentPage': currentPage,
        'registerUserForm': registerUserForm
    }
    return render(request, 'base/login_register.html', context)


# logout用户
def logoutUser(request):

    # 使用logout(request)方法来logout用户
    logout(request)

    # logout用户后，跳转到loginUser路由的页面
    return redirect('login')

# 根据messageId删除message
# 只有登录用户才能删除message
@login_required(login_url='login')
def deleteComment(request, messageId):
    comment = Message.objects.get(id = messageId)

    # 如果登录的用户不是该message的主人
    if request.user != comment.user:
        return HttpResponse('You are not allowed to delete others comments!')

    # 如果登录的用户是该message的主人，且请求是POST请求
    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    # base/templates/base/delete.html是共用的UI
    return render(request, 'base/delete.html', { 'obj': comment })

# 根据userId查询user
def userProfile(request, userId):

    user = User.objects.get(id = userId)
    rooms = user.room_set.all()
    roomComments = user.message_set.all()
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {
        'user': user,
        'rooms': rooms,
        'roomComments': roomComments,
        'topics': topics,
        'room_count': room_count,
    }

    return render(request, 'base/profile.html', context)

# 根据userId更新user
@login_required(login_url = 'login')
def userProfileUpdate(request):
    currentUser = request.user

    # 渲染数据到form上
    userForm = UserForm(instance = currentUser)

    # 如果访问此controller的请求是POST请求，说明用户要update信息
    if request.method == 'POST':
        updatedUser = UserForm(request.POST, instance = currentUser)

        if updatedUser.is_valid():
            updatedUser.save()
            return redirect('userProfile', userId = currentUser.id)

    context = {
        'userForm': userForm
    }

    return render(request, 'base/update-user.html', context)


