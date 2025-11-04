import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Weather App", layout="centered")
st.title("🌤 Weather Checker")

# User input: city name
city = st.text_input("Enter a city name:")

if city:
    # OpenWeatherMap API setup
    api_key = "YOUR_API_KEY_HERE"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["main"]  # e.g., Rain, Clear, Clouds

        # Output temperature
        st.write(f"🌡 Temperature: {temp} °C")

        # Output raining or not
        if weather.lower() == "rain":
            st.write("☔ It is raining 🌧")
        else:
            st.write("☀ No rain ☀")
    else:
        st.error("City not found. Please enter a valid city name.")
