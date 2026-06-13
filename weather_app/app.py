"""The weather app: a tiny Tkinter window backed by the OpenWeatherMap API.

I built this to learn how to drive a REST API from a desktop GUI. You type a German
postal code, the app asks OpenWeatherMap for the current conditions, and it shows the
city, a short description, the temperature in Fahrenheit, and the matching weather icon.

The OpenWeatherMap logic is split into small, side-effect-free helpers so the parsing
can be tested without a network connection or a display.
"""

from __future__ import annotations

import configparser
import os
import sys
import tkinter as tk
from pathlib import Path

import requests
from PIL import Image, ImageTk

# OpenWeatherMap endpoints. I request imperial units so temperatures come back in
# Fahrenheit, which is what the UI labels expect.
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "https://openweathermap.org/img/w/{icon}.png"

# I originally wrote this for Germany, so postal codes are always looked up there.
COUNTRY_CODE = "de"

# A neutral icon to show before the first lookup, and the messages the UI displays.
DEFAULT_ICON = "13n"
INVALID_POST_CODE = "Sorry, invalid post code :("

# Where the downloaded icons are cached on disk, relative to the working directory.
DEFAULT_ICON_PATH = "default.jpg"
CURRENT_ICON_PATH = "current_weather.jpg"

# I ship the API key in this file rather than in source, so it stays out of the
# public repo but still travels inside the packaged build.
CONFIG_FILENAME = "config.ini"


def _config_search_paths() -> list[Path]:
    """Return the places to look for ``config.ini``, most specific first.

    PyInstaller unpacks bundled data into ``sys._MEIPASS`` at runtime, so I check
    there first for the packaged build; when running from source the file lives at
    the project root or the current working directory.
    """
    paths: list[Path] = []
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir:
        paths.append(Path(bundle_dir) / CONFIG_FILENAME)
    paths.append(Path(__file__).resolve().parent.parent / CONFIG_FILENAME)
    paths.append(Path.cwd() / CONFIG_FILENAME)
    return paths


def _read_key_from_config(paths: list[Path]) -> str | None:
    """Return the API key from the first readable config file, or ``None``."""
    parser = configparser.ConfigParser()
    for path in paths:
        if path.is_file():
            parser.read(path)
            key = parser.get("openweathermap", "api_key", fallback="").strip()
            if key:
                return key
    return None


def get_api_key() -> str:
    """Return the OpenWeatherMap API key.

    I check the ``OPENWEATHER_API_KEY`` environment variable first so I can override
    the key while developing, then fall back to the bundled ``config.ini`` that ships
    inside the packaged app.
    """
    key = os.environ.get("OPENWEATHER_API_KEY")
    if key:
        return key

    key = _read_key_from_config(_config_search_paths())
    if key:
        return key

    raise RuntimeError(
        "No OpenWeatherMap API key found. Set the OPENWEATHER_API_KEY environment "
        "variable, or add your key to config.ini (see config.ini.example)."
    )


def fetch_weather(post_code: str, api_key: str, *, country_code: str = COUNTRY_CODE) -> dict:
    """Look up the current weather for a postal code and return the parsed response."""
    params = {
        "appid": api_key,
        "units": "imperial",
        "zip": f"{post_code},{country_code}",
    }
    return requests.get(WEATHER_URL, params=params).json()


def describe_weather(data: dict) -> tuple[str, str | None]:
    """Turn an OpenWeatherMap response into ``(status_text, icon_code)``.

    OpenWeatherMap returns a ``message`` field when something went wrong (for example
    an unknown postal code), so I treat that as the error case and report it with no
    icon to switch to.
    """
    if "message" in data:
        return INVALID_POST_CODE, None

    city = data["name"]
    description = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    temperature = f"{data['main']['temp']}° F"
    return f"{city}\n{description}\n{temperature}", icon


def load_icon(icon_code: str, path: str) -> ImageTk.PhotoImage:
    """Download a weather icon, cache it to ``path``, and return a Tk-ready image.

    The icons are PNGs; I convert to RGB so Tk can display them regardless of the
    source mode.
    """
    response = requests.get(ICON_URL.format(icon=icon_code))
    with open(path, "wb") as icon_file:
        icon_file.write(response.content)

    image = Image.open(path).convert("RGB")
    return ImageTk.PhotoImage(image)


class WeatherApp:
    """The Tkinter window and its event handlers."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

        self.root = tk.Tk()
        self.root.title("Simple Weather App")
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)
        self.root.geometry("350x200")

        self.status = tk.StringVar(value="Your weather right now?")
        tk.Message(self.root, textvariable=self.status, width=200).grid(row=1, column=1)

        # Keep a reference to the PhotoImage on the instance; Tk does not hold one
        # itself, so the image would otherwise be garbage collected and not shown.
        self._icon = load_icon(DEFAULT_ICON, DEFAULT_ICON_PATH)
        self.icon_label = tk.Label(self.root, image=self._icon)
        self.icon_label.grid(row=1, column=2)

        prompt = tk.Label(self.root, text="Enter your postal code to find out\ne.g. 52062")
        prompt.grid(row=3, column=1, sticky="E")

        self.entry = tk.Entry(self.root)
        self.entry.grid(row=3, column=2, pady=10)
        self.entry.bind("<Return>", lambda event: self.update_weather())

        tk.Button(self.root, text="Go!", command=self.update_weather).grid(row=4, column=2)

        note = tk.Label(self.root, text="PS: I've built this app to work for Germany only for now!")
        note.grid(column=1, columnspan=2, pady=20)

    def update_weather(self) -> None:
        """Look up the weather for the entered postal code and refresh the window."""
        data = fetch_weather(self.entry.get(), self._api_key)
        status_text, icon = describe_weather(data)
        self.status.set(status_text)

        if icon is not None:
            self._icon = load_icon(icon, CURRENT_ICON_PATH)
            self.icon_label.configure(image=self._icon)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    WeatherApp(get_api_key()).run()


if __name__ == "__main__":
    main()
