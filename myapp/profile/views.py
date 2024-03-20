from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from boardworld.serializers import MyUserSerializer
from myapp.forms import UserCreationForm
from myapp.models import MyUser


class MyLogin(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
            return reverse('main_page')


class MyLogout(LoginRequiredMixin, LogoutView):
    login_url = 'login'

    def get_success_url(self):
        return reverse('main_page')


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'form_registration.html'
    success_url = reverse_lazy('main_page')


class MyUserModelViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [AllowAny]
