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
                    vertical_spacing=0.35,  # הגדלת המרווח בין התרשימים
                    specs=[[{"type": "domain"}], [{"type": "domain"}]]
                )

                # מד טמפרטורה
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=temp if temp is not None else 0,
                        number={'suffix': " °C"},
                        gauge={
                            'axis': {'range': [0, 40]},
                            'bar': {'color': "orange" if temp is not None and temp > 30 else "blue"},
                            'steps': [
                                {'range': [0, 15], 'color': "lightblue"},
                                {'range': [15, 25], 'color': "lightgreen"},
                                {'range': [25, 40], 'color': "lightcoral"}
                            ]
                        }
                    ),
                    row=1, col=1
                )

                # מד לחות
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=humidity if humidity is not None else 0,
                        number={'suffix': " %"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "green" if humidity is not None and humidity < 70 else "red"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightyellow"},
                                {'range': [50, 80], 'color': "lightblue"},
                                {'range': [80, 100], 'color': "lightgray"}
                            ]
                        }
                    ),
                    row=2, col=1
                )

                # התאמת פריסה להגבהת הכותרת
                fig.update_layout(
                    height=800,  # הגדלת גובה התרשים
                    title_text=f"נתוני מזג אוויר ב־{name}",
                    title_y=0.95,  # הזזת הכותרת הראשית כלפי מעלה
                    margin=dict(l=50, r=50, t=120, b=50),  # הגדלת המרווח העליון
                    font=dict(family="Arial", size=14)
                )

                # התאמת מיקום כותרות המשנה (subplot titles)
                fig.update_annotations(
                    yshift=20  # הזזת כותרות המשנה כלפי מעלה
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