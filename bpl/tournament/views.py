from dateutil.utils import today
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .match_point_handler import prepare_final_match_point_df
from .models import MatchPoint, Tournament


# Create your views here.
@login_required
@require_http_methods(["GET"])
def tournaments_list(request):
    tournaments = Tournament.objects.all()
    return render(request, "tournaments/tournaments_dashboard.html", {"tournaments": tournaments})


@login_required
@require_http_methods(["GET"])
def match_points(request):
    prepare_final_match_point_df(request)
    # yesterday = datetime.now() - timedelta(days=1)
    _match_points = MatchPoint.objects.filter(match_date=today()).order_by("-total_points")
    return render(request, "tournaments/match_points.html", context={"match_points": _match_points})
