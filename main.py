import pandas as pd
import seaborn as sns
import streamlit as st
import datetime as dt
import pytz
import requests
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- הזן כאן את מפתח ה-API שלך (או החלף במשתנה סביבה בעצמך) ---
api_key = "053b9baa6643509be5a052798faf7f3b"

# --- הגדרות ממשק קצרות ---
st.set_page_config(page_title="בדיקת מזג האוויר", layout="centered")
st.markdown(
    """
    <style>
    html, body, [class*="css"] { direction: rtl; text-align: right; }
    .stButton, .stImage { margin-top: 8px; margin-bottom: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("בדיקת מזג האוויר")

# --- קלט משתמש ---
location = st.text_input("הזן את המיקום שלך (למשל: Tel Aviv)")

if st.button("בדוק מזג אוויר"):
    if not location.strip():
        st.error("אנא הזן מיקום תקין")
    else:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": api_key, "units": "metric", "lang": "he"}

        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            st.error(f"שגיאת חיבור או תגובה מה-API: {e}")
        else:
            data = r.json()
            if data.get("cod") == "404":
                st.error("העיר לא נמצאה. אנא בדוק את שם המיקום.")
            else:
                name = data.get("name", "—")
                weather = data.get("weather", [{}])[0]
                icon = weather.get("icon")
                desc = weather.get("description", "")
                temp = data.get("main", {}).get("temp")
                humidity = data.get("main", {}).get("humidity")

                st.write(f"**עיר**: {name}")
                if icon:
                    st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100, caption=f"תיאור: {desc}")

                st.write(f"**טמפרטורה**: {temp:.1f}°C" if temp is not None else "**טמפרטורה**: —")
                st.write(f"**לחות**: {humidity}% " if humidity is not None else "**לחות**: —")

                # --- Subplots אנכיים לשני המדדים (לא יחפפו) ---
                fig = make_subplots(
                    rows=2,
                    cols=1,
                    subplot_titles=("טמפרטורה (°C)", "לחות (%)"),
                    vertical_spacing=0.25,
                    specs=[[{"type": "domain"}],
                           [{"type": "domain"}]]
                )

                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=temp if temp is not None else 0,
                        number={'suffix': " °C"},
                        gauge={...}
                    ),
                    row=1, col=1
                )

                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=humidity if humidity is not None else 0,
                        number={'suffix': " %"},
                        gauge={...}
                    ),
                    row=2, col=1
                )

                fig.update_layout(
                    height=700,
                    title_text=f"נתוני מזג אוויר ב־{name}",
                    margin=dict(l=50, r=50, t=80, b=50),
                    font=dict(family="Arial", size=14)
                )

                st.plotly_chart(fig, use_container_width=True)

                # התראות מותנות
                if temp is not None:
                    if temp > 30:
                        st.warning("⚠️ טמפרטורה גבוהה! היזהר/י מהחום.")
                    elif temp < 15:
                        st.info("❄️ טמפרטורה נמוכה! כדאי להתלבש חם.")
                if humidity is not None and humidity > 80:
                    st.warning("💧 לחות גבוהה! ייתכן שיהיה דביק.")
