import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Weather App", layout="centered")
st.title("🌤 Weather Checker")

# Input: city name
city = st.text_input("Enter a city name:")

if city:
    # OpenWeatherMap API
    api_key = "482b8f9d1330689c2a4569cd9a857a16"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["main"]  # e.g., Rain, Clear, Clouds

        # Display temperature
        st.write(f"🌡 Temperature in {city}: {temp} °C")

        # Check if raining
        if "rain" in weather.lower():
            st.write("☔ It is raining 🌧")
        else:
            st.write("☀ No rain ☀")
    else:
        st.error("City not found. Please enter a valid city name.")
