from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from boardworld.serializers import GoodsSerializer
from myapp.forms import PurchaseForm
from myapp.models import Goods, Purchase
from django.urls import reverse, reverse_lazy
from django.db.models import F, QuerySet
from django.contrib import messages
from django.shortcuts import render

# class GoodsListView(ListView):
#     model = Goods
#     template_name = 'goods_list.html'
#     context_object_name = "goods"
#     paginate_by = 5
#
#     # def get(self, request, *args, **kwargs):
#     #     messages.add_message(request, messages.INFO, 'Hello world.')
#     #     return super().get(request, *args, *kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['create_form'] = PurchaseForm()
#         return context
#
#
#
# class GoodsDetailView(DetailView):
#     model = Goods
#     template_name = "goods_details.html"
#     context_object_name = "goods"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['pk'] = self.kwargs['pk']
#         context['create_form'] = PurchaseForm()
#         return context
#
#
# class GoodsUpdateView(UpdateView):
#     model = Goods
#     fields = ['name', 'description', 'price', 'quantity']
#     template_name = 'goods_update.html'
#     success_url = '/'
#     context_object_name = 'product'
#
#
# class GoodsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     template_name = "create_goods.html"
#     model = Goods
#     fields = ['name', 'description', 'price', 'quantity']
#     success_url = reverse_lazy('main_page')
#     success_message = "Product created successfully"
#     login_url = 'login'



class GoodsModelViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]


