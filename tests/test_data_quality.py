
import pandas as pd


def test_distance_quality_flag():
    distances = pd.Series([2.5, 0, -1.2])

    flags = distances.apply(
        lambda distance: "REVIEW" if distance <= 0 else "PASS"
    )

    assert flags.tolist() == ["PASS", "REVIEW", "REVIEW"]


def test_fare_quality_flag():
    fares = pd.Series([15.50, 0, -5.00])

    flags = fares.apply(
        lambda fare: "REVIEW" if fare < 0 else "PASS"
    )

    assert flags.tolist() == ["PASS", "PASS", "REVIEW"]
