#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   模型定义

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = db_managed` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
#from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.core.mail import send_mail
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.crypto import get_random_string, salted_hmac


db_prefix='wp_'
db_managed=True

USER_STATUS=(
    (1,'active'),
    (0,'inactive')
)
STATUS = (
    ('closed', '关闭'),
    ('open', '打开'),
)
POST_STATUS = (
    ('draft', '垃圾'),
    ('inherit', 'inherit'),
    ('private', '私有'),
    ('publish', '已发布'),
)
POST_TYPE = (
    ('attachment', '附件'),
    ('page', '页面'),
    ('post', '文章'),
    ('revision', 'revision'),
    ('nav_menu_item','导航菜单')
)
POST_MIME_TYPE=(
    ('markdown','markdown'),
    ('image/gif','image/gif'),
    ('text/html','text/html '),
    ('text/plain','text/plain'),

)
APPROVED_TYPE=(
    ('1','同意'),
    ('0','未审核'),
    ('spam','垃圾'),
    ('trash','回收站'),
)
TAXONOMY_TYPE=(
    ('category','文章分类'),
    ('post_tag','文章标签'),
    ('post_format','post_format'),
    ('link_category','链接分类'),
    )

VISIBLE_TYPE=(
    ('Y','可见'),
    ('N','私有'),
    )
TARGET_TYPE=(
    ('_blank','新建立窗口'),
    ('_top','弹出'),
    ('_none','同窗口')
    )


class Options(models.Model):
    option_id = models.AutoField(primary_key=True)
    option_name = models.CharField(verbose_name='名称', unique=True, max_length=64)
    option_value = models.TextField(verbose_name='值')
    autoload = models.CharField(verbose_name='自动加载' ,default='',blank=True,max_length=20)
    class Meta:
        managed = db_managed
        db_table = db_prefix+'options'
        verbose_name=u'可选'
        verbose_name_plural = u'可选管理'
    def __unicode__(self):
        return u'id[%s] %s' % (self.option_id,self.option_name)    

    
class Usermeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'usermeta'


class MyUserManager(BaseUserManager):
    def _create_user(self, user_login, user_email, user_pass,
                     is_staff, is_superuser, **extra_fields):
        if not user_login:
            raise ValueError('Users must have an user name')

        user = self.model(
            user_email=self.normalize_email(user_email),
            user_login=user_login,
            is_staff=is_staff,
            is_superuser=is_superuser,
            user_status=1,
        )

        user.set_password(user_pass)
        user.save(using=self._db)
        return user

    def create_user(self, user_login, user_email=None, password=None, **extra_fields):
        return self._create_user(user_login, user_email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, user_login, user_email, password, **extra_fields):
        return self._create_user(user_login, user_email, password, True, True,
                                 **extra_fields)


class MyAbstractBaseUser(models.Model):
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def has_usable_password(self):
        return is_password_usable(self.user_pass)

    def get_full_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_full_name() method')

    def get_short_name(self):
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_short_name() method.')

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.user_pass).hexdigest()


class Users(MyAbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True,unique=True) 
    user_login = models.CharField(max_length=60,unique=True,verbose_name='登录名')
    user_pass = models.CharField(max_length=164,verbose_name='密码')
    user_nicename = models.CharField(max_length=50,blank=True,verbose_name='昵称')
    user_email = models.CharField(max_length=100,blank=True,verbose_name='email')
    user_url = models.CharField(max_length=100,blank=True,verbose_name='网站')
    user_registered = models.DateTimeField(default=timezone.now,blank=True,verbose_name='注册时间')
    user_activation_key = models.CharField(max_length=60,blank=True)
    user_status = models.IntegerField(choices=USER_STATUS,default=0,verbose_name='状态',blank=True)
    display_name = models.CharField(max_length=250,blank=True,verbose_name='显示名字')
    is_staff = models.BooleanField(_('staff status'),default=False,blank=True)
    last_login = models.DateTimeField(_('last login'), default=timezone.now,blank=True)

    USERNAME_FIELD='user_login'
    REQUIRED_FIELDS = ['user_email']

    objects = MyUserManager()

    def set_password(self, raw_password):
        self.user_pass = make_password(raw_password)
    
    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["user_pass"])
        return check_password(raw_password, self.user_pass, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.user_pass = make_password(None)

    #############
    def get_full_name(self):
        # The user is identified by their email address
        return self.user_nicename

    def get_short_name(self):
        # The user is identified by their email address
        return self.display_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ 
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_active(self):
        return self.user_status
    

    def __unicode__(self):
        return u'%s' % (self.user_nicename)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'users'
        verbose_name=u'用户'
        verbose_name_plural = u'用户管理'


class Posts(models.Model):
    id=models.AutoField(primary_key=True) 
    post_author = models.ForeignKey(Users,db_column='post_author',verbose_name='作者')
    post_date = models.DateTimeField(verbose_name='发布时间',default=datetime.datetime.now,blank=True)
    post_date_gmt = models.DateTimeField(default=timezone.now,blank=True)
    post_content = models.TextField(verbose_name='内容')
    post_title = models.CharField(max_length=120,verbose_name='标题')
    post_excerpt = models.TextField(default='',blank=True)
    post_status = models.CharField(verbose_name='发布状态',choices=POST_STATUS,max_length=20)
    comment_status = models.CharField(default='',blank=True,max_length=20)
    ping_status = models.CharField(verbose_name='ping状态',default='',blank=True,max_length=20)
    post_password = models.CharField(default='',blank=True,max_length=20)
    post_name = models.CharField(default='',blank=True,max_length=200)
    to_ping = models.TextField(default='',blank=True)
    pinged = models.TextField(default='',blank=True)
    post_modified = models.DateTimeField(default=datetime.datetime.now,blank=True)
    post_modified_gmt = models.DateTimeField(default=timezone.now,blank=True)
    post_content_filtered = models.TextField(default='',blank=True)
    post_parent = models.BigIntegerField(default=0,blank=True)
    guid = models.CharField(max_length=255,default='',blank=True)
    menu_order = models.IntegerField(default=0,blank=True)
    post_type = models.CharField(verbose_name='发布类型',choices=POST_TYPE,max_length=20)
    post_mime_type = models.CharField(verbose_name='文档类型',choices=POST_MIME_TYPE,max_length=100)
    comment_count = models.BigIntegerField(default=0,blank=True)
    def __unicode__(self):
        return u'%s' % (self.post_title)

    #@models.permalink
    def get_absolute_url(self):
        if self.post_type =='post':
            return reverse('blog.views.article', args=[str(self.id)])
        elif self.post_type =='page':
            return reverse('blog.views.page', args=[str(self.id)])
        else:
            return reverse('blog.views.article', args=[str(self.id)])


    class Meta:
        managed = db_managed
        db_table = db_prefix+'posts'
        verbose_name=u'发布'
        verbose_name_plural = u'发布管理'

class Postmeta(models.Model):
    meta_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posts,db_column='post_id')
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.meta_id)
    class Meta:
        managed = db_managed
        db_table = db_prefix+'postmeta'
        verbose_name=u'发布附带'
        verbose_name_plural = u'发布管理'


class Commentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'commentmeta'


class Comments(models.Model):
    comment_id=models.AutoField(primary_key=True)
    comment_post=models.ForeignKey(Posts,verbose_name='文章')
    comment_author = models.CharField(max_length=100,verbose_name='评论者')
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200,blank=True)
    comment_author_ip = models.CharField(default='',max_length=100,blank=True)  # Field name made lowercase.
    comment_date = models.DateTimeField(verbose_name='评论日期',default=datetime.datetime.now,blank=True)
    comment_date_gmt = models.DateTimeField(default=timezone.now,blank=True)
    comment_content = models.TextField(verbose_name='评论内容')
    comment_karma = models.IntegerField(default=0)
    comment_approved = models.CharField(verbose_name='审核情况',choices=APPROVED_TYPE,max_length=20,default=0)
    comment_agent = models.CharField(default='',max_length=255,blank=True)
    comment_type = models.CharField(default='',max_length=20,blank=True)
    comment_parent = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)


    def get_absolute_url(self):
        if self.comment_post.post_type =='post':
            return '/blog/?p=%s#comment-%s'%(self.comment_post.id,self.comment_id)
        elif self.comment_post.post_type =='page':
            return '/blog/page/%s#comment-%s'%(self.comment_post.id,self.comment_id)
        else:
            return '/blog/?p=%s#comment-%s'%(self.comment_post.id,self.comment_id)
    
    class Meta:
        managed = db_managed
        db_table = db_prefix+'comments'
        verbose_name=u'评论'
        verbose_name_plural = u'评论管理'

        permissions = (
            ("can_comment_direct", "can_comment_direct"),
            ("can_comment_unlimit_time",'不限制时间评论')
        )

    def __unicode__(self):
        return u'%s'% (self.comment_id)
    

class Terms(models.Model):
    term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='分类名')
    slug = models.CharField(unique=True, max_length=200, verbose_name='缩略名')
    term_group = models.BigIntegerField(default=0, verbose_name='分组号')
    def __str__(self):
        return self.name
      
    class Meta:
        managed = db_managed
        db_table = db_prefix + 'terms'
        verbose_name = '目录/标签'
        verbose_name_plural = '目录/标签管理'


class TermTaxonomy(models.Model):
    term_taxonomy_id = models.AutoField(primary_key=True)
    term = models.ForeignKey(Terms,verbose_name='目录/标签')
    taxonomy = models.CharField(max_length=32,choices=TAXONOMY_TYPE,verbose_name='分类方法(category/post_tag)')
    description = models.TextField(verbose_name='分类描述')
    parent = models.BigIntegerField(default=0,verbose_name='父分类id')
    count = models.BigIntegerField(default=0,verbose_name='数量统计')
    def __str__(self):
        return '%s ->%s(%s)' % (self.taxonomy,self.term.name,self.description)
    
    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_taxonomy'
        verbose_name = '目录/标签分类'
        verbose_name_plural = '目录/标签分类管理'


class Links(models.Model):
    link_id = models.AutoField(primary_key=True)
    link_url = models.CharField(max_length=255,verbose_name='URL链接')
    link_name = models.CharField(max_length=255,verbose_name='名称')
    link_image = models.CharField(default='',blank=True,max_length=255,verbose_name='图片')
    link_target = models.CharField(default='',blank=True,max_length=25,choices=TARGET_TYPE,verbose_name='打开方式')
    link_description = models.CharField(default='',blank=True,max_length=255,verbose_name='描述')
    link_visible = models.CharField(default='Y',blank=True,max_length=20,choices=VISIBLE_TYPE,verbose_name='是否可见')
    link_owner = models.BigIntegerField(default=0,blank=True,verbose_name='拥有者')
    link_rating = models.IntegerField(default=0,blank=True,verbose_name='排名')
    link_updated = models.DateTimeField(default=datetime.datetime.now,blank=True,verbose_name='更新日期')
    link_rel = models.CharField(default='',blank=True,max_length=255)
    link_notes = models.TextField(default='',blank=True,verbose_name='备注')
    link_rss = models.CharField(default='',blank=True,max_length=255,verbose_name='RSS链接')
    class Meta:
        managed = db_managed
        db_table = db_prefix+'links'
        verbose_name=u'链接'
        verbose_name_plural = u'链接管理'

    def __unicode__(self):
        return u'%s  链接:%s' % (self.link_name,self.link_url)

class PostLinkeManager(models.Manager):
    def get_queryset(self):
        
        ret=super(PostLinkeManager, self).get_queryset().filter()
        return ret

class TermRelationships(models.Model):
    term_relationship_id=models.AutoField(primary_key=True)
    object=models.ForeignKey(Posts,verbose_name='文章')
    object_link=models.ForeignKey(Links,null=True,verbose_name='链接',db_column='object_link')

    #term_taxonomy_id = models.BigIntegerField()
    term_taxonomy = models.ForeignKey(TermTaxonomy,verbose_name='分类/标签')
    term_order = models.IntegerField(default=0,verbose_name='排序')
    objects=PostLinkeManager()

    def __unicode__(self):
        return u'%s 属于 %s分类' % (self.object_id,self.term_taxonomy.term.name)
    
    def object_link(self):
        return self.object
   

    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_relationships'
        verbose_name_plural=u'文章/链接分类管理'
        verbose_name=u'文章/链接分类'



#manager all models
class Manager(object):
    """docstring for Manager"""
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_instance'):
            o=super(Manager,cls)
            cls._instance=o.__new__(cls,*args,**kwargs)
            cls.instances={}
        return cls._instance

    def _get_class(self,cls=''):
            module_name=''
            class_name=''
            ws=cls.rsplit('.',1)
            if len(ws)==2:
                (module_name, class_name) = ws
            else:
                class_name=ws[0]
                module_name= __file__ and os.path.splitext(os.path.basename(__file__))[0] 
            print(module_name)
            module_meta = __import__(module_name, globals(), locals(), [class_name]) 
            class_meta = getattr(module_meta, class_name) 
            cls=class_meta 
            return cls

    def __init__(self, cls=None,*args,**kwargs):
        #print '#####init self=',self.__class__.__name__,' cls:',cls
        self.cls=cls
        self.args=args
        self.kwargs=kwargs
        if cls==None:
            return
        if isinstance(cls,str):
            cls=self._get_class(cls)
        elif isinstance(cls,cls.__class__):
            self.instances[cls.__class__]=cls
            self.cls=cls.__class__
            return
        if cls in self.instances:
            self=self.instances[cls] 
        else:
            obj=cls(*args,**kwargs)
            self.instances[cls]=obj
            self=obj

    def instance(self,cls=None,*args,**kwargs):
        #print 'membermethod'
        try:
            if cls==None:
                if self.cls==None:
                    return self
                cls=self.cls
            if isinstance(cls,str):
                cls=self._get_class(cls)
            if cls in self.instances:
                return self.instances[cls]
            else:
                #print 'instance no found',type(cls),args,kwargs
                obj=cls(*args,**kwargs)
                self.instances[cls]=obj
                return obj
        except TypeError as e:
            return cls
        except AttributeError as e:
            return  cls
        except Exception as e:
            return e

    @classmethod
    def inst(cls,clz=None,*args,**kwargs):
        if clz==None:
            if cls==None:
                return cls()
            clz=cls
        return cls(clz,*args,**kwargs).instance(*args,**kwargs)

    @staticmethod
    def ins(cls=None,*args,**kwargs):
        return Manager(cls,*args,**kwargs).inst(cls,*args,**kwargs) 

    @classmethod
    def add_member_method(self,cls,fun,*args,**kwargs):
        obj=self.instance(cls,*args,**kwargs);
        setattr(obj,fun.__name__,type.MethodType(fun,obj))
        return obj

    @classmethod
    def add_static_method(self,cls,fun,*args,**kwargs):
        obj=self.instance(cls,*args,**kwargs)
        setattr(obj,fun.__name__,fun)
        return obj

    @classmethod
    def add_class_method(self):
        pass

    def get_head_info(self):
        class HeadInfo:
            def __init__(self,blogname,blogdescription,title='邪恶二进制'):
                self.blogname=blogname
                self.blogdescription=blogdescription
                self.title=title
        blogname=Options.objects.filter(option_name='blogname').last()
        if blogname!=None:
            blogname=blogname.option_value
        else:
            blogname=''

        blogdescription=Options.objects.filter(option_name='blogdescription').last()
        if blogdescription!=None:
            blogdescription=blogdescription.option_value
        else:
            blogdescription=''
        
        info =HeadInfo(blogname,blogdescription)       
        return info

    def get_all_links(self):
        links=Links.objects.filter(link_visible='Y')
        cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('link_category',),term_taxonomy__count__gt=0)
        all_links={}
        all_opt={}
        for l in links:
            for c in cats:
                if(c.object_id==l.link_id):
                    if(c.term_taxonomy.term.term_id in all_opt):
                        all_links[c.term_taxonomy.term.term_id].append(l)
                    else:
                        all_links[c.term_taxonomy.term.term_id]=[l,]   
                    all_opt[c.term_taxonomy.term.term_id]=c
        return all_links,all_opt
        pass
