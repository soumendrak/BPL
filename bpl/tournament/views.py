from dateutil.utils import today
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from bpl.tournament.standing_handler import fetch_standings

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
    date = request.GET.get("date", today())
    prepare_final_match_point_df(request)
    _match_points = MatchPoint.objects.filter(match_date=date).order_by("-total_points")
    return render(request, "tournaments/match_points.html", context={"match_points": _match_points})


@login_required
@require_http_methods(["GET"])
def standing(request):
    standing = fetch_standings(request)
    # standing = standing.to_html(index=False)
    print(f"standing: {standing}")
    return render(request, "tournaments/standing.html", context={"standing": standing})
