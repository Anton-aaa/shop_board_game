from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from myapp.forms import PurchaseForm
from myapp.models import Goods, Purchase
from django.urls import reverse, reverse_lazy
from django.db.models import F, QuerySet
from django.contrib import messages


class CreatePurchaseView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    http_method_names = ['post']
    form_class = PurchaseForm
    success_url = reverse_lazy('goods_list')
    success_message = "Purchase completed successfully"
    template_name = 'goods_list.html'

    def form_valid(self, form):
        client = self.request.user
        new_purchase = form.save(commit=False)
        new_purchase.client = client
        product = Goods.objects.get(id=self.kwargs['pk'])
        new_purchase.product = product

        if form.cleaned_data['purchase_quantity'] < 1:
            messages.add_message(self.request, messages.ERROR,
                                 'The quantity of goods to purchase must be greater than 0.')

            return HttpResponseRedirect(reverse('goods_list'))

        if form.cleaned_data['purchase_quantity'] * product.price > client.wallet:
            messages.add_message(self.request, messages.ERROR,
                                 'There are not enough funds in your wallet to purchase.')

            return HttpResponseRedirect(reverse('goods_list'))

        if product.quantity - form.cleaned_data['purchase_quantity'] < 0:
            messages.add_message(self.request, messages.ERROR,
                                 'There is no such quantity of goods.')

            return HttpResponseRedirect(reverse('goods_list'))

        product.quantity = F('quantity') - form.cleaned_data['purchase_quantity']
        product.save()

        client.wallet = F('wallet') - form.cleaned_data['purchase_quantity'] * product.price
        client.save()

        new_purchase = form.save()
        return super().form_valid(form)

class PurchaseListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Purchase
    template_name = 'purchases_list.html'
    context_object_name = "purchases"
    paginate_by = 5


    def get_queryset(self):
        if self.queryset is not None:
            queryset = Purchase.objects.filter(client=self.request.user)
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = Purchase.objects.filter(client=self.request.user)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset