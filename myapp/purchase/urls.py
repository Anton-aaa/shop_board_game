from django.urls import path
from .views import (
    CreatePurchaseView,
    PurchaseListView
)

urlpatterns = [
    path('purchase/<int:pk>/', CreatePurchaseView.as_view(), name="create_purchase"),
    path('all_purchase', PurchaseListView.as_view(), name="purchase_list"),
]