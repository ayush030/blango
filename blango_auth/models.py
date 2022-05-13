from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

from django.utils.translation import gettext_lazy as _
# Create your models here.

# we’ll use django.contrib.auth.models.UserManager as a guide to implementing our methods, generally just replacing the use of username with email.
class BlangoUserManager(UserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError("Email must be set")
    
     # For email addresses, foo@bar.com and foo@BAR.com are equivalent; the domain part is case-insensitive according to the RFC specs. Normalizing means providing a canonical representation, so that any two equivalent email strings normalize to the same thing.
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)

    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("super user must have is_staff=True")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("super user must have is_superuser=True")
    
    return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
  username = None
  
  # translation strings. They tell Django: “This text should be translated into the end user’s language, if a translation for this text is available in that language.” 
  email = models.EmailField(_("email address"), unique=True,)
  
  objects = BlangoUserManager()

  USERNAME_FIELD = "email"  # by default is unique and required
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
