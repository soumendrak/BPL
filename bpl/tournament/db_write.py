from dateutil.utils import today

from .models import Fixture


def get_scorecard_url():
    # Read `scorecard_url` column from fixture table and call read_webpage function
    return Fixture.objects.get(match_date=today())
