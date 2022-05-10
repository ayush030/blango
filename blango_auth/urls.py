from django.urls import path, include
from .views import profile


from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm


urlpatterns=[
  # django default user registration system
  # path('', include('django.contrib.auth.urls')),

  # django_registration library
  path('', include('django_registration.backends.activation.urls')),

  path('profile/', profile, name='profile'),
  path("register/", RegistrationView.as_view(form_class=BlangoRegistrationForm), name="django_registration_register",),
]