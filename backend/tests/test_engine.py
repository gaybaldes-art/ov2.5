import pytest

from app.engine import forecast, score_matrix


def test_score_matrix_is_normalized():
    matrix = score_matrix(1.45, 1.1)
    assert sum(map(sum, matrix)) == pytest.approx(1.0)


def test_one_x_two_probabilities_sum_to_one():
    result = forecast(1.45, 1.1)
    p = result["probabilities"]
    assert p["home_win"] + p["draw"] + p["away_win"] == pytest.approx(1.0, abs=2e-5)


def test_totals_are_complements():
    p = forecast(1.45, 1.1)["probabilities"]
    assert p["over_2_5"] + p["under_2_5"] == pytest.approx(1.0, abs=2e-5)


def test_invalid_expected_goals_are_rejected():
    with pytest.raises(ValueError):
        forecast(-0.1, 1.0)
