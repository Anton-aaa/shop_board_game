from django.urls import path, include
from rest_framework import routers
from .views import (
                   MyLogin,
                   MyLogout,
                   Register,
                   MyUserModelViewSet
                   )

router = routers.SimpleRouter()
router.register("user", MyUserModelViewSet)

urlpatterns = [
    path('login/', MyLogin.as_view(), name="login"),
    path("logout/", MyLogout.as_view(), name="logout"),
    path('registration/', Register.as_view(), name="register"),
    path('', include(router.urls)),
]