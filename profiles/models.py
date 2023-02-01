from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class ProfileUserManager(BaseUserManager):
    def create_user(self, email: str, first_name: str, password: str):
        if not email or not first_name or not password:
            return None

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str, password: str):
        user = self.create_user(email, first_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class Profile(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ProfileUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)