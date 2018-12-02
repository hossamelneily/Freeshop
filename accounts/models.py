from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self,email,full_name,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("User should have Email")
        if not password:
            raise ValueError("User should have password")

        if not full_name:
            raise ValueError("Full name isn't exists")

        user = self.model(
            email=self.normalize_email(email)      #decapatilize email
        )
        user.FullName=full_name
        user.set_password(password)

        user.is_active=is_active
        user.staff=is_staff
        user.admin=is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self,email,full_name,password=None):
        user=self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=True,

        )
        return user

    # def create_superuser(self,email,FullName,password=None):
    #     user=self.create_user(
    #         email=email,
    #         full_name=FullName,
    #         password=password,
    #         is_staff=True,
    #         is_admin=True
    #     )
    #     return user

    def create_superuser(self,*args,**kwargs):
        email = kwargs.get('email')
        fullname = kwargs.get('FullName')
        password= kwargs.get('password')
        self.create_user(email,fullname,password,is_active=True,is_staff=True,is_admin=True)



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    FirstName = models.CharField(verbose_name='First Name',max_length=255,blank=True,null=True)
    LastName = models.CharField(verbose_name='Last Name',max_length=255,blank=True,null=True)
    FullName = models.CharField(verbose_name='Full Name',max_length=255,blank=True,null=True)
    gender = models.CharField(blank=True,null=True,max_length=100)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    country = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['FullName',]   #python manage.py createsuperuser here will make effect  // username_field and password will be required by default

    objects=UserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True


    def get_full_name(self):
        return self.FullName

    @property
    def is_staff(self):
        return self.staff

    # @property
    # def is_active(self):
    #     return self.active

    @property
    def is_admin(self):
        return self.admin
# using=self._db   #Managers use that parameter to define on which database the underlying queryset the manager uses should operate on.
