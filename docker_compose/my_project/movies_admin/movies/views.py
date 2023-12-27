"""Still unused file."""

from django.shortcuts import render


def index(request):
    """Return default page from request."""
    return render(request, 'index.html')
