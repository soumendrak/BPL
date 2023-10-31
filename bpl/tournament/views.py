from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Tournament


# Create your views here.
@login_required
@require_http_methods(["GET"])
def tournaments_list(request):
    tournaments = Tournament.objects.all()
    return render(request, "tournaments/tournaments_dashboard.html", {"tournaments": tournaments})
