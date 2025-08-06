import pandas as pd
import streamlit as st
import datetime as dt
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- הזן כאן את מפתח ה-API שלך ---
api_key = "053b9baa6643509be5a052798faf7f3b"

# --- הגדרות ממשק ---
st.set_page_config(page_title="החזאי העולמי", layout="centered")
st.markdown(
    """
    <style>
    /* כיוון כתיבה מימין לשמאל (עברית) */
    html, body, [class*="css"] {
        direction: rtl;
    }

    /* ממרכז את כל התוכן בדף */
    .block-container {
        text-align: center !important;
    }

    /* עיצוב כפתור ומרכזתו */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin: 0 auto;
        display: block;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stButton > button:active {
        transform: scale(0.95);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* ממרכז תמונה ותיאור שלה */
    .stImage {
        display: block;
        margin: 0 auto;
    }
    .stImage > figure {
        margin: 0 auto;
        text-align: center !important; /* <-- ממרכז את התמונה והכיתוב */
        direction: rtl;
    }
    .stImage > figure > img {
        display: inline-block;
        margin: 0 auto;
    }
    .stImage > figure > figcaption {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center !important; /* <-- מבטיח כיתוב ממורכז */
        display: block;
        width: 100%;
        direction: rtl;
        font-size: 14px;
    }

    /* אופציונלי: הקטנת ריווח אנכי כדי שיהיה נקי יותר */
    .stImage, .stButton, .stMarkdown {
        margin-top: 8px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ברוכים הבאים לשירות החזאי העולמי")


# --- פונקציה לקבלת תחזית ל-5 ימים ---
def get_5day_forecast(location, api_key):
    """
    מבצע קריאה ל-API של OpenWeatherMap כדי לקבל תחזית ל-5 ימים.
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",
        "lang": "he"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"שגיאה בקבלת התחזית ל-5 ימים: {e}")
        return None


# --- קלט משתמש ---
location = st.text_input("הזינו את המיקום לבדיקת מזג האוויר (למשל: דולב / Paris)")

if st.button("לחצו כאן לבדיקת מזג אוויר"):
    if not location.strip():
        st.error("אנא הזינו מיקום תקין")
    else:
        # קריאה למזג אוויר נוכחי
        url_current = "http://api.openweathermap.org/data/2.5/weather"
        params_current = {"q": location, "appid": api_key, "units": "metric", "lang": "he"}

        try:
            r_current = requests.get(url_current, params=params_current, timeout=10)
            r_current.raise_for_status()
        except requests.RequestException as e:
            st.error(f"שגיאת חיבור או תגובה מה-API: {e}")
        else:
            data_current = r_current.json()
            if data_current.get("cod") == "404":
                st.error("העיר לא נמצאה. אנא בדוק את שם המיקום.")
            else:
                name = data_current.get("name", "—")
                weather = data_current.get("weather", [{}])[0]
                icon = weather.get("icon")
                desc = weather.get("description", "")
                temp = data_current.get("main", {}).get("temp")
                humidity = data_current.get("main", {}).get("humidity")

                st.write(f"**המיקום שהזנתם הוא**: {name}")
                st.write(f"**קשה לחשוב על מיקום מדהים יותר מ-** {name}")
                if icon:
                    st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=100, caption=f"תיאור: {desc}")

                st.write(f"**טמפרטורה**: {temp:.1f}°C" if temp is not None else "**טמפרטורה**: —")
                st.write(f"**לחות**: {humidity}% " if humidity is not None else "**לחות**: —")

                # --- תרשימים ---
                fig = make_subplots(
                    rows=2,
                    cols=1,
                    subplot_titles=("טמפרטורה (°C)", "לחות (%)"),
                    vertical_spacing=0.35,
                    specs=[[{"type": "domain"}], [{"type": "domain"}]]
                )

                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=temp if temp is not None else 0,
                        number={'suffix': " °C", 'valueformat': ".0f"},
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

                fig.update_layout(
                    height=800,
                    title_text=f"נתוני מזג אוויר ב־{name}",
                    title_x=0.5,
                    title_y=0.95,
                    title_xanchor="center",
                    margin=dict(l=50, r=50, t=120, b=50),
                    font=dict(family="Arial", size=14)
                )

                fig.update_annotations(yshift=20)

                st.plotly_chart(fig, use_container_width=True)

                if temp is not None:
                    if temp > 30:
                        st.warning("⚠️ הטמפרטורה כעת גבוהה! היזהרו מהחום.")
                    elif temp < 15:
                        st.info("❄️ הטמפרטורה כעת נמוכה! כדאי להתלבש חם.")
                if humidity is not None and humidity > 80:
                    st.warning("💧 הלחות כעת גבוהה! ייתכן שיהיה דביק.")

                # --- תחזית ל-5 ימים הקרובים ---
                forecast_data = get_5day_forecast(location, api_key)

                if forecast_data and "list" in forecast_data:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("## תחזית ל-5 ימים הקרובים")

                    daily_forecasts = {}
                    for forecast in forecast_data['list']:
                        # קבוצות הנתונים מגיעות כל 3 שעות
                        # נשתמש בתאריך לסיכום הנתונים היומיים
                        date_str = dt.datetime.fromtimestamp(forecast['dt']).strftime('%A, %d/%m')

                        if date_str not in daily_forecasts:
                            daily_forecasts[date_str] = {
                                'temp_min': forecast['main']['temp_min'],
                                'temp_max': forecast['main']['temp_max'],
                                'weather_desc': forecast['weather'][0]['description'],
                                'icon': forecast['weather'][0]['icon']
                            }
                        else:
                            # נעדכן את הטמפרטורה המינימלית והמקסימלית ליום
                            if forecast['main']['temp_min'] < daily_forecasts[date_str]['temp_min']:
                                daily_forecasts[date_str]['temp_min'] = forecast['main']['temp_min']
                            if forecast['main']['temp_max'] > daily_forecasts[date_str]['temp_max']:
                                daily_forecasts[date_str]['temp_max'] = forecast['main']['temp_max']

                    # הצגת הנתונים באמצעות עמודות
                    cols = st.columns(len(daily_forecasts))

                    for i, (date_str, data) in enumerate(daily_forecasts.items()):
                        with cols[i]:
                            st.markdown(f"**{date_str}**")
                            st.image(f"https://openweathermap.org/img/wn/{data['icon']}@2x.png", width=50)
                            st.markdown(f"**מקס'**: {data['temp_max']:.1f}°C")
                            st.markdown(f"**מיני'**: {data['temp_min']:.1f}°C")
                            st.markdown(f"**מצב**: {data['weather_desc']}")