import pandas as pd
import seaborn as sns
import streamlit as st
import datetime as dt
import pytz
import requests
import json

# הגדרת כותרת לאפליקציה
st.title("דירוג הקושי של הצום")

# קבלת קלט טקסט מהמשתמש
user_name = st.text_input("מה שמך?", "אורח/ת")

# הצגת ברכה מותאמת אישית
st.write(f"שלום, {user_name}! כיף לראות אותך כאן.")

# הוספת סליידר לבחירת מספר
selected_number = st.slider(
    "דרג את הקושי של הצום בין 1 [קל] ל-10 [קשה]",
    min_value=1,
    max_value=10,
    value=5 # ערך ברירת מחדל
)

# הצגת המספר שנבחר
st.write(f"בחרת את המספר: {selected_number}")

if selected_number <= 4:
    st.write("כנראה בגלל שהצום אחרי שבת היה קל יחסית")
else:
    st.write("בגלל שהצום אחרי שבת היה אמור להיות קל יחסית")

# הוספת כפתור
if st.button("אשמח להביא את הגאולה ולחסוך את הצום"):
    st.success("כדי להביא את הגאולה עלינו להאיר את העולם בתורה ובמעשים טובים")

# הוספת טקסט תחתון
st.caption("זוהי אפליקציה פשוטה להדגמה של Streamlit.")

print("Just testing Git Desktop")