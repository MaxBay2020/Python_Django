from django.db import models
from django.contrib.auth.models import User

# 创建Topic表
# 如果不明确指定主键，会自动按顺序生成主键，如1,2,3...
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



# 创建Room表
class Room(models.Model):

    # name字段的类型是字符串，最大长度是200；
    name = models.CharField(max_length=200)

    # description字段的类型是字符串；
    # TextField和CharField都是用来设置字符串类型的，但TextField比CharField要大；
    # 默认情况null的值是False；
    # blank设置的是view中的form中的此字段可以为空；
    description = models.TextField(null=True, blank=True)

    # participants和room是多对多的关系
    # 因此room表和user表已经建立了多对一的关系，即下面的host字段；
    # 如果还想和user表建立多对多的关系，需要加上第二个参数：related_name='participants'
    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    # auto_now的意思是每次update的时候都会记录时间；
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add的意思是只在create的时候记录时间；
    created = models.DateTimeField(auto_now_add=True)

    # 和Topic表是多对一的关系
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # 和user是多对一的关系
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 使用下面的代码对room的查询进行排序
    # -updated表示降序；如果写成updated，则表示升序；
    class Meta:
        ordering = ['-updated', '-created']

    # 当我们打印此表格的某个record时，返回的是此record的name字段的值；
    def __str__(self):
        return self.name

# 创建Message表
class Message(models.Model):
    # 和user表是多对一的关系
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 和Room表创建关联，是多对一的关系；
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # auto_now的意思是每次update的时候都会记录时间；
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add的意思是只在create的时候记录时间；
    created = models.DateTimeField(auto_now_add=True)

    # 使用下面的代码对message的查询进行排序
    # -updated表示降序；如果写成updated，则表示升序；
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]