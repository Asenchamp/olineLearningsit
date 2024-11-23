from django.shortcuts import render
from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return render(request, 'csrf_error.html', status=403)
