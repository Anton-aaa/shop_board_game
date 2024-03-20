from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from myapp.models import ReturnGoods, Purchase
from django.urls import reverse, reverse_lazy
from django.db.models import F


class CreateReturnGoodsView(LoginRequiredMixin, SuccessMessageMixin, View):
    login_url = 'login'
    http_method_names = ['post']
    success_message = "Return request has been successfully created"

    def post(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(id=self.kwargs['pk'])
        return_goods = ReturnGoods.objects.create(purchase=purchase)
        return HttpResponseRedirect(reverse('purchase_list'))

    # def form_valid(self, form):
    #     return_goods = form.save(commit=False)
    #     return_goods.product = Purchase.objects.get(id=self.kwargs['pk'])
    #     return_goods = form.save()
    #     return super().form_valid(form)


class DeleteReturnGoodsView(LoginRequiredMixin, DeleteView):
    model = ReturnGoods
    success_url = '/'
    login_url = 'login'



class ReturnGoodsListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ReturnGoods
    template_name = 'return_goods_list.html'
    context_object_name = "return_goods"
    paginate_by = 5


class SuccessReturnGoodsView(LoginRequiredMixin, SuccessMessageMixin, View):
    login_url = 'login'
    http_method_names = ['post']
    success_message = "Return request has been successfully created"

    def post(self, request, *args, **kwargs):
        return_goods = ReturnGoods.objects.get(id=self.kwargs['pk'])
        purchase = return_goods.purchase
        client = purchase.client
        product = purchase.product

        client.wallet = F('wallet') + purchase.purchase_quantity * product.price
        client.save()

        product.quantity = F('quantity') + purchase.purchase_quantity
        product.save()

        purchase.delete()

        return HttpResponseRedirect(reverse('return_goods_list'))


