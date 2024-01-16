from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

#custom UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, name, OTP , password=None, confirm_password=None):
        """
        Creates and saves a User with the given email, name , and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            is_active=0,
            OTP=OTP,
            login_id= self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            is_active=1,
            login_id = email
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200) 
    login_id = models.CharField(max_length=255,default=email,unique=True)
    image = models.CharField(max_length=500,null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    OTP = models.IntegerField(null=True)
    OTP_generation_time = models.DateTimeField(auto_now_add=True)
    meta_data = models.TextField(null=True)
    remarks = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)
    

    objects = UserManager()

    USERNAME_FIELD = "login_id"
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

