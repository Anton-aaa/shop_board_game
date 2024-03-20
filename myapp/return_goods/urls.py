from django.urls import path
from .views import (
    CreateReturnGoodsView,
    DeleteReturnGoodsView,
    ReturnGoodsListView,
    SuccessReturnGoodsView
)

urlpatterns = [
    path('create/<int:pk>/', CreateReturnGoodsView.as_view(), name="create_return_goods"),
    path('list', ReturnGoodsListView.as_view(), name="return_goods_list"),
    path('delete/<int:pk>/', DeleteReturnGoodsView.as_view(), name="delete_return_goods"),
    path('success_return_goods/<int:pk>/', SuccessReturnGoodsView.as_view(), name="success_return"),
]