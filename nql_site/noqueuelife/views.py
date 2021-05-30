from django.views import generic

from orders.models import Order


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_orders_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Order.objects.order_by('-pub_date')[:9]
