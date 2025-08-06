import pandas as pd
import seaborn as sns
import streamlit as st
import datetime as dt
import pytz
import requests
import json
import plotly.graph_objects as go

# הוספת CSS לכיווניות RTL
st.markdown("""
<style>
body {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# כותרת לממשק
st.title("בדיקת מזג האוויר")

# קבלת קלט מיקום מהמשתמש
location = st.text_input("הזן את המיקום שלך (למשל, Tel Aviv):", "")

# הגדרת מפתח ה-API
api_key = "053b9baa6643509be5a052798faf7f3b"

# הוספת כפתור להפעלת הבקשה
if st.button("בדוק מזג אוויר"):
    if location.strip() == "":
        st.error("אנא הזן מיקום תקין")
    else:
        # הגדרת כתובת ה-URL עם יחידות ושפה
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&lang=he"

        # שליחת בקשת GET
        response = requests.get(url)

        # בדיקת התגובה
        if response.status_code == 200:
            data = response.json()
            if data.get("cod") == "404":
                st.error("העיר לא נמצאה. אנא בדוק את שם המיקום.")
            else:
                # קבלת קוד האייקון מה-API
                icon_code = data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

                # הצגת הנתונים כטקסט עם האייקון
                st.write(f"**עיר**: {data['name']}")
                st.image(icon_url, width=100, caption=f"תיאור: {data['weather'][0]['description']}")
                st.write(f"**טמפרטורה**: {data['main']['temp']:.1f}°C")
                st.write(f"**לחות**: {data['main']['humidity']}%")

                # יצירת ויזואליזציה עם Plotly
                fig = go.Figure()

                # הוספת מד טמפרטורה
                fig.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=data['main']['temp'],
                    title={'text': "טמפרטורה (°C)"},
                    gauge={'axis': {'range': [0, 40]},
                           'bar': {'color': "orange" if data['main']['temp'] > 30 else "blue"},
                           'steps': [
                               {'range': [0, 15], 'color': "lightblue"},
                               {'range': [15, 25], 'color': "lightgreen"},
                               {'range': [25, 40], 'color': "lightcoral"}]}
                ))

                # הוספת מד לחות
                fig.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=data['main']['humidity'],
                    title={'text': "לחות (%)"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "green" if data['main']['humidity'] < 70 else "red"},
                           'steps': [
                               {'range': [0, 50], 'color': "lightyellow"},
                               {'range': [50, 80], 'color': "lightblue"},
                               {'range': [80, 100], 'color': "lightgray"}]}
                ))

                # הגדרת פריסה עם כיווניות RTL
                fig.update_layout(
                    title=f"נתוני מזג אוויר ב{data['name']}",
                    font=dict(family="Arial", size=14),
                    margin=dict(l=150, r=50, t=50, b=50),  # התאמת מרווחים ל-RTL
                )

                # הצגת הגרף
                st.plotly_chart(fig)

                # הוספת התראות מותנות
                if data['main']['temp'] > 30:
                    st.warning("⚠️ טמפרטורה גבוהה! היזהר מחום.")
                elif data['main']['temp'] < 15:
                    st.info("❄️ טמפרטורה נמוכה! כדאי להתלבש חם.")
                if data['main']['humidity'] > 80:
                    st.warning("💧 לחות גבוהה! ייתכן שיהיה דביק.")
        else:
            st.error(f"שגיאה: קוד {response.status_code}. בדוק את מפתח ה-API או חיבור לאינטרנט.")