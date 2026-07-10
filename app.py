import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Dashboard")
st.markdown("### Analyze student performance using interactive charts.")

# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

df = pd.read_csv("data/student-por.csv")

# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

df["Average"] = (df["G1"] + df["G2"] + df["G3"]) / 3

df["Result"] = df["Average"].apply(
    lambda x: "Pass" if x >= 10 else "Fail"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🎓 Student Dashboard")
st.sidebar.markdown("---")
st.sidebar.header("📌 Filters")

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["sex"].unique())
)

school = st.sidebar.selectbox(
    "Select School",
    ["All"] + sorted(df["school"].unique())
)

filtered_df = df.copy()

if gender != "All":
    filtered_df = filtered_df[
        filtered_df["sex"] == gender
    ]

if school != "All":
    filtered_df = filtered_df[
        filtered_df["school"] == school
    ]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

total_students = len(filtered_df)

average_marks = round(
    filtered_df["Average"].mean(), 2
)

highest_marks = filtered_df["G3"].max()

pass_percentage = round(
    (filtered_df["Result"] == "Pass").mean() * 100,
    2
)

fail_percentage = round(
    (filtered_df["Result"] == "Fail").mean() * 100,
    2
)

st.subheader("📊 Dashboard Summary")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric("👨‍🎓 Total Students", total_students)

with k2:
    st.metric("📊 Average Grade", average_marks)

with k3:
    st.metric("🏆 Highest Grade", highest_marks)

with k4:
    st.metric("✅ Pass %", f"{pass_percentage}%")

with k5:
    st.metric("❌ Fail %", f"{fail_percentage}%")

# ---------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head(),
    use_container_width=True,
    height=220
)

st.markdown("---")

# ---------------------------------------------------
# ROW 1
# ---------------------------------------------------

col1, col2 = st.columns(2)

# ---------------- Gender ----------------


with col1:

    st.subheader("📊 Gender Performance")

    gender_avg = (
        filtered_df.groupby("sex")["Average"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        gender_avg,
        x="sex",
        y="Average",
        color="sex",
        color_discrete_sequence=["#ff69b4", "#4dabf7"],
        text_auto=".2f",
        title="Average Grade by Gender"
    )

    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Average Grade",
        height=420,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- Pass Fail ----------------

with col2:

    st.subheader("🥧 Pass vs Fail")

    result = (
    filtered_df["Result"]
    .value_counts()
    .reset_index()
    )

    result.columns = ["Result", "Count"]

    fig2 = px.pie(
    result,
    names="Result",
    values="Count",
    color="Result",
    color_discrete_map={
        "Pass": "#2ecc71",
        "Fail": "#e74c3c"
    },
    hole=0.35
)

    fig2.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

    fig2.update_layout(
    title="Pass vs Fail",
    height=420,
    showlegend=False
)

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
# ---------------------------------------------------
# ROW 2
# ---------------------------------------------------

col3, col4 = st.columns(2)

# ---------------- Grade Distribution ----------------

with col3:

    st.subheader("📈 Grade Distribution")

    fig3 = px.histogram(
    filtered_df,
    x="Average",
    nbins=10,
    color_discrete_sequence=["orange"],
    title="Grade Distribution"
)

    fig3.update_layout(
    xaxis_title="Average Grade",
    yaxis_title="Students",
    height=420
)

    st.plotly_chart(fig3, use_container_width=True)
# ---------------- Internet Access ----------------

with col4:

    st.subheader("🌐 Internet Access")

    internet_avg = (
    filtered_df.groupby("internet")["Average"]
    .mean()
    .reset_index()
)

    fig4 = px.bar(
    internet_avg,
    x="internet",
    y="Average",
    color="internet",
    color_discrete_sequence=["coral", "mediumseagreen"],
    text_auto=".2f",
    title="Average Grade by Internet Access"
)

    fig4.update_layout(
    xaxis_title="Internet Access",
    yaxis_title="Average Grade",
    height=420,
    showlegend=False
)

    st.plotly_chart(fig4, use_container_width=True)

    st.info(
    "Students with internet access generally have higher average grades than students without internet access."
) 


# -------------------------------------------------
# Correlation Heatmap
# -------------------------------------------------

st.markdown("---")
st.subheader("🔥 Correlation Heatmap")

numeric = filtered_df.select_dtypes(include="number")

fig5, ax5 = plt.subplots(figsize=(10, 7))

sns.heatmap(
    numeric.corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    square=True,
    cbar=True,
    annot_kws={"size":8},
    ax=ax5
)

ax5.set_title(
    "Correlation Matrix",
    fontsize=16,
    fontweight="bold",
    pad=15
)

plt.xticks(
    rotation=45,
    ha="right",
    fontsize=9
)

plt.yticks(
    rotation=0,
    fontsize=9
)

plt.tight_layout()

st.pyplot(fig5)

st.markdown("---")

# ---------------------------------------------------
# TOP 10 STUDENTS
# ---------------------------------------------------

st.subheader("🏆 Top 10 Students")

top_students = (
    filtered_df
    .sort_values(by="Average", ascending=False)
    .head(10)
    .round(2)
)

st.dataframe(
    top_students[
        ["school","sex","G1","G2","G3","Average"]
    ],
    use_container_width=True,
    height=390
)

st.markdown("---")

st.subheader("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="student_performance_filtered.csv",
    mime="text/csv"
)

st.success("✅ Dashboard completed successfully!")

#st.markdown("---")
#st.markdown(
#"""
#<div style="text-align:center;color:#9ca3af;font-size:14px">
#Built by <b>Isha Rawat</b> | Student Performance Dashboard | Python • Pandas • Streamlit
#</div>
#"""
#unsafe_allow_html=True
#)

