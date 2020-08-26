from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

LANG_CHOICES = (
    ('de', 'German'),
    ('en', 'English'),
)

from main.helpers import hashstring  # noqa: E402


def upload_path(instance, filename):
    return f'{hashstring(instance.user.username)}/{filename}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.profile_image = None
        user.username = email
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """ Representing an application user

    Default fieldsets: Permissions, Personal info, Important dates

    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True)

    language = models.CharField(
        null=False,
        default="en",
        max_length=255,
        choices=LANG_CHOICES,
    )
    language.fieldset = 'Personal info'
    language.is_registration = True
    language.is_custom = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    pass

    def __str__(self):
        if not self.first_name and not self.last_name:
            return self.email
        return self.first_name + ' ' + self.last_name


class ProfileImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    upload_name = models.CharField(max_length=255)
    upload = models.FileField(upload_to=upload_path)
    user = models.OneToOneField(CustomUser,
                                related_name='profile_image',
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile image: {self.user.username}"

    class Meta:
        verbose_name = 'Profile Image'
        verbose_name_plural = 'Profile Images'
