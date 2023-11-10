from datetime import datetime, timedelta

import pytest
from models import Fixture

from .db_write import get_scorecard_url


@pytest.mark.django_db
def test_get_scorecard_url():
    # Setup
    yesterday = datetime.now() - timedelta(days=1)
    Fixture.objects.create(
        match_date=yesterday, scorecard_url="https://www.espncricinfo.com/ci/engine/match/1384424.html"
    )

    # Call the function
    result = get_scorecard_url()

    # Assert
    assert result == ["http://test.com"]
