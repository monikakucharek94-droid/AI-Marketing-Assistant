import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="AI Strategy Hub", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #94a3b8;
    margin-bottom: 1rem;
}
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #2d3748;
    box-shadow: 0 8px 24px rgba(0,0,0,0.16);
}
.metric-label {
    color: #cbd5e1;
    font-size: 0.9rem;
}
.metric-value {
    color: white;
    font-size: 1.8rem;
    font-weight: 800;
}
.section-card {
    background: #111827;
    border: 1px solid #253047;
    border-radius: 18px;
    padding: 20px;
    margin-top: 10px;
}
.recommendation-box {
    background: #0f172a;
    border-left: 4px solid #22c55e;
    padding: 14px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

data = [
    ["Customer Support Chatbot", 9, 4, 8, 5, 120000],
    ["Marketing Content Generator", 8, 3, 9, 4, 90000],
    ["Customer Review Analysis", 7, 3, 8, 3, 70000],
    ["Sales Forecasting", 9, 7, 6, 6, 150000],
    ["Churn Prediction", 8, 8, 5, 7, 180000],
    ["Document Search Assistant", 7, 5, 7, 4, 95000],
]

df = pd.DataFrame(
    data,
    columns=[
        "Use Case",
        "Business Value",
        "Implementation Difficulty",
        "AI Readiness",
        "Risk Level",
        "Estimated Annual Value"
    ]
)

df["Priority Score"] = (
    df["Business Value"] * 0.35
    + df["AI Readiness"] * 0.30
    + (10 - df["Implementation Difficulty"]) * 0.20
    + (10 - df["Risk Level"]) * 0.15
).round(2)

def classify_phase(score):
    if score >= 7.5:
        return "Phase 1 - Quick Win"
    elif score >= 6.3:
        return "Phase 2 - Scale"
    return "Phase 3 - Strategic Bet"

df["Roadmap Phase"] = df["Priority Score"].apply(classify_phase)

st.markdown('<div class="main-title">🧠 AI Strategy Hub</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Portfolio project for AI Manager roles • Prioritize AI use cases, assess ROI, risk and implementation readiness</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">AI Use Cases</div>
        <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    top_priority = df["Priority Score"].max()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Top Priority Score</div>
        <div class="metric-value">{top_priority}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    total_value = int(df["Estimated Annual Value"].sum())
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Potential Annual Value</div>
        <div class="metric-value">${total_value:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    quick_wins = (df["Roadmap Phase"] == "Phase 1 - Quick Win").sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Quick Wins</div>
        <div class="metric-value">{quick_wins}</div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("AI Use Case Portfolio")
    st.dataframe(df, use_container_width=True, height=350)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Priority Score by Use Case")

    fig, ax = plt.subplots(figsize=(7, 4))
    sorted_df = df.sort_values("Priority Score", ascending=True)
    ax.barh(sorted_df["Use Case"], sorted_df["Priority Score"])
    ax.set_xlabel("Priority Score")
    ax.set_ylabel("Use Case")
    ax.set_title("AI Prioritization Overview")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Quick Wins vs Strategic Bets")

    quick_win_df = df[df["Roadmap Phase"] == "Phase 1 - Quick Win"]
    scale_df = df[df["Roadmap Phase"] == "Phase 2 - Scale"]
    strategic_df = df[df["Roadmap Phase"] == "Phase 3 - Strategic Bet"]

    st.write("**Phase 1 - Quick Wins**")
    for item in quick_win_df["Use Case"]:
        st.write(f"✅ {item}")

    st.write("**Phase 2 - Scale**")
    for item in scale_df["Use Case"]:
        st.write(f"📈 {item}")

    st.write("**Phase 3 - Strategic Bets**")
    for item in strategic_df["Use Case"]:
        st.write(f"🧠 {item}")

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Risk vs Value Overview")

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.scatter(df["Risk Level"], df["Estimated Annual Value"])

    for _, row in df.iterrows():
        ax2.annotate(row["Use Case"], (row["Risk Level"], row["Estimated Annual Value"]), fontsize=8)

    ax2.set_xlabel("Risk Level")
    ax2.set_ylabel("Estimated Annual Value")
    ax2.set_title("Risk vs Business Value")
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Executive Recommendation")

top_projects = df.sort_values("Priority Score", ascending=False).head(3)

recommendations = [
    f"Start with **{top_projects.iloc[0]['Use Case']}** because it combines high business value with strong AI readiness.",
    f"Add **{top_projects.iloc[1]['Use Case']}** as a second-wave initiative to scale visible AI impact across the business.",
    f"Use **{top_projects.iloc[2]['Use Case']}** as part of the broader transformation roadmap.",
    "Focus Phase 1 on quick wins that build internal trust in AI before moving to more complex use cases.",
    "Create a governance model covering data quality, AI risk, adoption and ROI measurement."
]

for rec in recommendations:
    st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("AI Manager Notes")

selected_use_case = st.selectbox("Select a use case", df["Use Case"].tolist())

selected_row = df[df["Use Case"] == selected_use_case].iloc[0]

st.write(f"**Business Value:** {selected_row['Business Value']}/10")
st.write(f"**Implementation Difficulty:** {selected_row['Implementation Difficulty']}/10")
st.write(f"**AI Readiness:** {selected_row['AI Readiness']}/10")
st.write(f"**Risk Level:** {selected_row['Risk Level']}/10")
st.write(f"**Estimated Annual Value:** ${selected_row['Estimated Annual Value']:,}")
st.write(f"**Recommended Phase:** {selected_row['Roadmap Phase']}")
st.write(f"**Priority Score:** {selected_row['Priority Score']}")

st.markdown('</div>', unsafe_allow_html=True)

st.caption("Built with Python, Streamlit, Pandas and Matplotlib • Portfolio project for AI Manager / AI Strategy / Digital Transformation roles")
