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
st.set_page_config(page_title="החזאי העולמי", layout="centered")
st.markdown(
    """
    <style>
    html, body, [class*="css"] { direction: rtl; text-align: right; }
    .stButton, .stImage { margin-top: 8px; margin-bottom: 8px; }
    /* עיצוב מותאם אישית לכפתור */
    .stButton > button {
        background-color: #4CAF50; /* צבע רקע ירוק */
        color: white; /* צבע טקסט לבן */
        padding: 12px 24px; /* ריווח פנימי */
        border: none; /* הסרת מסגרת */
        border-radius: 10px; /* פינות מעוגלות */
        font-size: 16px; /* גודל פונט */
        font-weight: bold; /* טקסט מודגש */
        cursor: pointer; /* סמן יד בעת ריחוף */
        transition: background-color 0.3s ease, transform 0.2s ease; /* אנימציה למעבר צבע והגדלה */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* צל קל */
    }
    .stButton > button:hover {
        background-color: #45a049; /* צבע כהה יותר בעת ריחוף */
        transform: scale(1.05); /* הגדלה קלה בעת ריחוף */
    }
    .stButton > button:active {
        transform: scale(0.95); /* הקטנה קלה בעת לחיצה */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* צל קטן יותר בעת לחיצה */
    }
    /* תיקון שבירת שורות בקפשן של התמונה */
    .stImage > .caption {
        white-space: nowrap; /* מונע שבירת שורות */
        max-width: 100%; /* מבטיח שהקפשן לא יחרוג מהתמונה */
        overflow: hidden; /* מסתיר טקסט שחורג */
        text-overflow: ellipsis; /* מוסיף שלוש נקודות אם הטקסט ארוך מדי */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("ברוכים הבאים לשירות החזאי העולמי")

# --- קלט משתמש ---
location = st.text_input("הזינו את המיקום לבדיקת מזג האוויר (למשל: דולב / Paris)")

if st.button("לחצו כאן לבדיקת מזג אוויר"):
    if not location.strip():
        st.error("אנא הזינו מיקום תקין")
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

                st.write(f"**המיקום שהזנתם הוא**: {name}")
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

                # מד לחות
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=humidity if temp is not None else 0,
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

                # התאמת פריסה למרכוז הכותרת ושמירה על RTL
                fig.update_layout(
                    height=800,  # הגדלת גובה התרשים
                    title_text=f"נתוני מזג אוויר ב־{name}",  # הכותרת הראשית
                    title_x=0.5,  # מרכוז הכותרת האופקי
                    title_y=0.95,  # הזזת הכותרת הראשית כלפי מעלה
                    title_xanchor="center",  # וידוא שהכותרת ממורכזת
                    margin=dict(l=50, r=50, t=120, b=50),  # הגדלת המרווח העליון
                    font=dict(family="Arial", size=14)  # גופן תומך עברית
                )

                # התאמת מיקום כותרות המשנה (subplot titles)
                fig.update_annotations(
                    yshift=20  # הזזת כותרות המשנה כלפי מעלה
                )

                st.plotly_chart(fig, use_container_width=True)

                # התראות מותנות
                if temp is not None:
                    if temp > 30:
                        st.warning("⚠️ הטמפרטורה כעת גבוהה! היזהרו מהחום.")
                    elif temp < 15:
                        st.info("❄️ הטמפרטורה כעת נמוכה! כדאי להתלבש חם.")
                if humidity is not None and humidity > 80:
                    st.warning("💧 הלחות כעת גבוהה! ייתכן שיהיה דביק.")