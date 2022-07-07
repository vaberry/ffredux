from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class NewDocument(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='img/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# default='uploads/profile_pictures/default_pic.png',
# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    teamname = models.CharField(default="*name your team*",max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="img/", default='img/default_user.png', blank=True)
    pick_spot = models.BigIntegerField(blank=True,null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Owner.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Post(models.Model):
    title = models.TextField(max_length=250,blank=True,null=True)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    pinned = models.BooleanField(default=False)

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

class CommAddFranchise(models.Model):
    manager = models.ForeignKey(User,on_delete=models.DO_NOTHING,default='',blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

class Pick(models.Model):
    original_owner = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='+')
    owner = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True,related_name='+')
    year = models.IntegerField()
    round = models.BigIntegerField()
    pick = models.BigIntegerField(blank=True,null=True)

class UpdateDraftSpot(models.Model):
    owner_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    updated_pick_spot = models.BigIntegerField(blank=True,null=True)

class Trade(models.Model):
    trader_one = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='traderone')
    trader_one_list = models.ManyToManyField(Pick,blank=True,related_name='traderonelist')
    trader_one_accepted = models.BooleanField(default=False)
    trader_two = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tradertwo')
    trader_two_list = models.ManyToManyField(Pick,blank=True,related_name='tradertwolist')
    trader_two_accepted = models.BooleanField(default=False)
    trade_date = models.DateTimeField(default=timezone.now)
    trade_status = models.CharField(default='In Talks',blank=True,null=True,max_length=20)
    flagged = models.BooleanField(default=False)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class Notification(models.Model):
	# 1 = Like, 2 = Comment, 3 = DM, 4 = trade proposal, 5= trade accepted, 6= trade rejected
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    trade = models.ForeignKey('Trade', on_delete=models.CASCADE, related_name='+', blank=True, null=True)