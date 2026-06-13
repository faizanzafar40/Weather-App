# A Simple Weather App

A small desktop weather app I built in Python with Tkinter. You type in a German
postal code and it asks the [OpenWeatherMap](https://openweathermap.org) API for the
current conditions, then shows the city, a short description, the temperature in
Fahrenheit, and the matching weather icon.

I wrote it as a learning project to get a feel for talking to a REST API from a
desktop GUI — handling the request, parsing the JSON, and updating the window with
the result (including downloading and displaying the weather icon).

## Built with

- **Python** with **Tkinter** for the GUI
- **[requests](https://requests.readthedocs.io/)** for the HTTP calls
- **[Pillow](https://python-pillow.org/)** to load and display the weather icons
- **[OpenWeatherMap API](https://openweathermap.org/current)** for the weather data

## Features

- Look up the current weather for a German city by postal code
- Shows the city name, a short description, and the temperature in Fahrenheit
- Displays the matching OpenWeatherMap weather icon
- Submit with the **Go!** button or by pressing **Enter**

## Screenshot

_Drop a screenshot of the running app here, e.g. `docs/screenshot.png`._

## Using the packaged build

If you just want to use the app, grab the build I share (the `.exe`) and run it —
the API key is bundled in, so there's nothing to configure. Type a German postal
code (for example `52062`) and press **Go!** or **Enter**.

## Running from source

- Python 3.8 or newer (Tkinter ships with the standard CPython installer)
- Install the dependencies:

  ```bash
  pip install -r requirements.txt
  ```

The app needs an OpenWeatherMap API key, which it looks for in two places, in order:

1. the `OPENWEATHER_API_KEY` environment variable, if set; otherwise
2. a `config.ini` file (copy `config.ini.example` to `config.ini` and paste your key in).

`config.ini` is gitignored so the key stays out of the repo, but it gets bundled into
the packaged build (see below). Get a free key by registering at
<https://openweathermap.org>.

```bash
# Option A — environment variable
#   Windows (PowerShell):  $env:OPENWEATHER_API_KEY = "your-api-key"
#   macOS / Linux:         export OPENWEATHER_API_KEY="your-api-key"

# Option B — config.ini
cp config.ini.example config.ini   # then edit it and add your key

python -m weather_app
```

Type a German postal code (for example `52062`) and press **Go!** or **Enter**.

## Running the tests

The tests cover the response-parsing logic and need no network or display:

```bash
pip install pytest
pytest
```

## Building a stand-alone executable

I use [PyInstaller](https://pyinstaller.org/) with the bundled spec file to produce
a single executable:

```bash
pip install pyinstaller
pyinstaller weather-app.spec
```

The spec bundles `config.ini` into the executable, so the build I share works out of
the box without anyone needing their own key. The result lands in `dist/`.

## Project structure

```
weather_app/        # the application package
  app.py            # GUI, OpenWeatherMap calls, and response parsing
  __main__.py       # entry point for `python -m weather_app`
tests/              # tests for the parsing logic
weather-app.spec    # PyInstaller build spec (bundles config.ini)
config.ini.example  # template for the API key config
pyproject.toml      # project metadata and tooling config
requirements.txt    # runtime dependencies
```

## Notes

This is one of my earlier learning projects, scoped to Germany on purpose to keep it
simple. Extending it to other countries is mostly a matter of changing the country
code that gets sent with the postal code lookup.

## License

Released under the [MIT License](LICENSE).
