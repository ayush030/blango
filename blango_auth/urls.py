from django.urls import path, include
from .views import profile


from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm


urlpatterns=[
  path('profile/', profile, name='profile'),
  path("register/", RegistrationView.as_view(form_class=BlangoRegistrationForm), name="django_registration_register",),

  # django_registration library
  path('', include('django_registration.backends.activation.urls')),


  # django default user registration system. #This is the package that includes all the inbuild django auth view. That also sets up the views from django.contrib.auth (login, logout, password reset, etc.).
  path('', include('django.contrib.auth.urls')),
]