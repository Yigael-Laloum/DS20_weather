import pandas as pd
import seaborn as sns
import streamlit as st
import datetime as dt
import pytz
import requests
import json

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
                st.write(f"**עיר**: {data['name']}")
                st.write(f"**תיאור**: {data['weather'][0]['description']}")
                st.write(f"**טמפרטורה**: {data['main']['temp']:.1f}°C")
                st.write(f"**לחות**: {data['main']['humidity']}%")
        else:
            st.error(f"שגיאה: קוד {response.status_code}. בדוק את מפתח ה-API או חיבור לאינטרנט.")