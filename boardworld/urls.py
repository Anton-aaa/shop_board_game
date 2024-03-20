from django.contrib import admin
from rest_framework.authtoken import views
from myapp.views import (
                         MyUserModelViewSet,
                         GoodsModelViewSet,
                         PurchaseModelViewSet,
                         ReturnGoodsModelViewSet
                         )
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register("user", MyUserModelViewSet)
router.register("goods", GoodsModelViewSet)
router.register("purchase", PurchaseModelViewSet)
router.register("return_goods", ReturnGoodsModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
]
