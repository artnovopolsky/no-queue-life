import copy

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Order, OrderMeta


class IndexView(generic.ListView):
    template_name = 'one-products.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Order.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Order
    template_name = 'one-products.html'


