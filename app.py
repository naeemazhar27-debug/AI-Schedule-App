import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.title("AI-Driven Construction Schedule Auto-Generator")

uploaded_file = st.file_uploader("Upload your Excel (Activity | Quantity | Predecessor | Crew Size | Productivity/day)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.write("### Input Data", df)

    # Compute durations
    df["Duration (days)"] = (df["Quantity"] / df["Productivity/day"]).apply(lambda x: max(1, round(x)))

    # Compute Start/Finish dates sequentially for demo
    start_date = datetime.today()
    start_dates = []
    finish_dates = []
    prev_finish = start_date

    for i, row in df.iterrows():
        if str(row["Predecessor"]).strip() == "-" or pd.isna(row["Predecessor"]):
            s = start_date
        else:
            s = prev_finish
        f = s + timedelta(days=row["Duration (days)"])
        start_dates.append(s.date())
        finish_dates.append(f.date())
        prev_finish = f

    df["Start Date"] = start_dates
    df["Finish Date"] = finish_dates

    st.write("### Generated Schedule", df)

    # Plot Gantt chart
    fig = px.timeline(df, x_start="Start Date", x_end="Finish Date", y="Activity", color="Activity")
    fig.update_yaxes(autorange="reversed")  # tasks top-down
    st.plotly_chart(fig)

    # Download output
    out_file = "AI_Schedule_Output.xlsx"
    df.to_excel(out_file, index=False)
    with open(out_file, "rb") as f:
        st.download_button("Download Schedule as Excel", f, file_name=out_file)
else:
    st.info("Upload an Excel file to start.")
