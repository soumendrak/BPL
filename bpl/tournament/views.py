from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from bpl.tournament.standing_handler import fetch_standings

from .models import MatchPoint, Tournament


# Create your views here.
class TournamentView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "tournaments/tournaments_dashboard.html"
    extra_context = {"tournaments": Tournament.objects.all()}


class MatchPointView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "tournaments/match_points.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = {"match_points": MatchPoint.objects.all()}
        return super().get(request, *args, **kwargs)


class StandingView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "tournaments/standing.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = {"standing": fetch_standings(request)}
        return super().get(request, *args, **kwargs)
