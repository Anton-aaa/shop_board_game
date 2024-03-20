from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages


class VisitCounter(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if 'counter_middleware' not in request.session:
                request.session['counter_middleware'] = 1

            if request.session['counter_middleware'] / 4 == 1:
                request.session['counter_middleware'] = 1
                messages.add_message(request, messages.INFO, 'It is 4!')
            else:
                request.session['counter_middleware'] += 1
