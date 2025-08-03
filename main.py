import pandas as pd
import seaborn as sns
import streamlit as st
import datetime as dt
import pytz
import requests
import json

# הגדרת כותרת לאפליקציה
st.title("ברוכים הבאים לאפליקציית הדוגמה שלי!")

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

# הוספת כפתור
if st.button("לחץ כאן"):
    st.success("לחצת על הכפתור!")

# הוספת טקסט תחתון
st.caption("זוהי אפליקציה פשוטה להדגמה של Streamlit.")

print("Just testing Git Desktop")