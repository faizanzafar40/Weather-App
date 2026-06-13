"""Tests for the OpenWeatherMap response parsing.

These cover the side-effect-free helpers, so they run without a network connection
or a display.
"""

from weather_app.app import INVALID_POST_CODE, _read_key_from_config, describe_weather


def test_describe_weather_formats_a_successful_lookup():
    data = {
        "name": "Aachen",
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "main": {"temp": 59.0},
    }

    status_text, icon = describe_weather(data)

    assert status_text == "Aachen\nclear sky\n59.0° F"
    assert icon == "01d"


def test_describe_weather_reports_an_error_response():
    data = {"cod": "404", "message": "city not found"}

    status_text, icon = describe_weather(data)

    assert status_text == INVALID_POST_CODE
    assert icon is None


def test_read_key_from_config_uses_the_first_file_with_a_key(tmp_path):
    config = tmp_path / "config.ini"
    config.write_text("[openweathermap]\napi_key = abc123\n")

    missing = tmp_path / "missing.ini"

    assert _read_key_from_config([missing, config]) == "abc123"


def test_read_key_from_config_returns_none_when_absent(tmp_path):
    assert _read_key_from_config([tmp_path / "nope.ini"]) is None
