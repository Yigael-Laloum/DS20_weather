# יצירת שתי עמודות
col1, col2 = st.columns(2)

with col1:
    # מד טמפרטורה
    fig_temp = go.Figure(go.Indicator(
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
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    # מד לחות
    fig_hum = go.Figure(go.Indicator(
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
    st.plotly_chart(fig_hum, use_container_width=True)
