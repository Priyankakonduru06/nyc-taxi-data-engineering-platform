
import pandas as pd

from src.process_data import (
    create_distance_quality_flag,
    create_fare_quality_flag,
)


def test_distance_quality_flag():
    distances = pd.Series([2.5, 0, -1.2])

    flags = create_distance_quality_flag(distances)

    assert flags.tolist() == ["PASS", "REVIEW", "REVIEW"]


def test_fare_quality_flag():
    fares = pd.Series([15.50, 0, -5.00])

    flags = create_fare_quality_flag(fares)

    assert flags.tolist() == ["PASS", "PASS", "REVIEW"]

def test_zero_fare_passes():
    fares = pd.Series([0.0])

    flags = create_fare_quality_flag(fares)

    assert flags.tolist() == ["PASS"]


def test_positive_distance_passes():
    distances = pd.Series([0.01])

    flags = create_distance_quality_flag(distances)

    assert flags.tolist() == ["PASS"]


def test_empty_inputs_return_empty_flags():
    distances = pd.Series([], dtype=float)
    fares = pd.Series([], dtype=float)

    assert create_distance_quality_flag(distances).empty
    assert create_fare_quality_flag(fares).empty

