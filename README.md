# Simple Weather App

## Brief Description

A simple weather desktop application built in Python which uses Tkinter and OpenWeatherMap API

## User Setup Guide

- Download this repository
- Navigate to **_dist/test.exe_**
- Execute the application
- Note: This weather app by default provides weather information for German cities by postal code. 

## Developer's Guide

- Weather data is provided by: https://openweathermap.org.
- An API key is required in order for this app to interact with OpenWeatherMap's API.
- To obtain an API key, you must first register at: https://openweathermap.org.
- Then modify the `test.py` file by copying your API key into the api_address variable definition.
- To create a stand-alone executable application, use pyinstaller with the included files.
- To modify locale and search parameters, read the OpenWeatherMap's API docs at: https://openweathermap.org/current
