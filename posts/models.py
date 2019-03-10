from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.db.models.signals import pre_save
from blogapi.utils import unique_slug_generator
from django.utils import timezone
# Create your models here.

class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).order_by('-timestamp')


class Post(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete='DO_NOTHING')
    title       = models.CharField(max_length=120)
    content     = models.TextField()
    slug        = models.SlugField(unique=True,blank=True,null=True)
    draft       = models.BooleanField(default=False)
    publish     = models.DateTimeField(auto_now=False,auto_now_add=False)
    image       = models.ImageField(upload_to='photos/%y/%m/%d', blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add= True, auto_now=False)
    updated     = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = PostManager()

    # class Meta: 
    #     order ing = ['-timestamp','-updated','-id']

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title


def post_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(post_pre_save_receiver,sender=Post)