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
    "בחר מספר בין 0 ל-100",
    min_value=0,
    max_value=100,
    value=50 # ערך ברירת מחדל
)

# הצגת המספר שנבחר
st.write(f"בחרת את המספר: {selected_number}")

# הוספת כפתור
if st.button("לחץ כאן"):
    st.success("לחצת על הכפתור!")

# הוספת טקסט תחתון
st.caption("זוהי אפליקציה פשוטה להדגמה של Streamlit.")

print("Just testing Git Desktop")