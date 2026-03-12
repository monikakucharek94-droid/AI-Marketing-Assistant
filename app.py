import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Customer Insights Pro",
    page_icon="🚀",
    layout="wide"
)

# ---------- STYLES ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #9aa0a6;
    font-size: 1rem;
    margin-bottom: 1.2rem;
}
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #2d3748;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
}
.metric-label {
    font-size: 0.9rem;
    color: #cbd5e1;
    margin-bottom: 0.35rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
}
.section-card {
    background: #111827;
    border: 1px solid #253047;
    border-radius: 20px;
    padding: 20px;
    margin-top: 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.16);
}
.small-note {
    color: #94a3b8;
    font-size: 0.9rem;
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

# ---------- DATA ----------
demo_reviews = [
    "This product is amazing and works perfectly.",
    "The delivery was very slow and disappointing.",
    "I love this cream, very good quality.",
    "Terrible packaging, the box arrived damaged.",
    "Very good quality and beautiful design.",
    "Not worth the price.",
    "Excellent results after one week of use.",
    "Customer service was disappointing.",
    "Great product, I will buy again.",
    "The package arrived damaged and late.",
    "Amazing formula, my skin feels better.",
    "The product is okay, but shipping was slow.",
]

positive_words = {
    "amazing", "love", "good", "excellent", "great", "beautiful",
    "perfect", "better", "best", "happy", "fantastic", "recommend"
}

negative_words = {
    "slow", "terrible", "not worth", "disappointing", "damaged",
    "late", "bad", "poor", "broken", "problem", "worst", "awful"
}

stopwords = {
    "the", "is", "a", "an", "and", "or", "to", "of", "for", "this", "that",
    "was", "were", "it", "my", "very", "after", "with", "but", "i", "will",
    "again", "arrived", "product", "use"
}

def detect_sentiment(text: str) -> str:
    text_lower = str(text).lower()

    pos_score = sum(1 for word in positive_words if word in text_lower)
    neg_score = sum(1 for word in negative_words if word in text_lower)

    if pos_score > neg_score:
        return "Positive"
    if neg_score > pos_score:
        return "Negative"
    return "Neutral"

def extract_keywords(series: pd.Series, top_n: int = 8):
    all_words = []
    for text in series.dropna().astype(str):
        cleaned = re.findall(r"[a-zA-Z]+", text.lower())
        words = [w for w in cleaned if w not in stopwords and len(w) > 2]
        all_words.extend(words)
    return Counter(all_words).most_common(top_n)

def build_demo_df():
    df = pd.DataFrame({"Review": demo_reviews})
    df["Sentiment"] = df["Review"].apply(detect_sentiment)
    return df

def normalize_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)

    # Try to find a review column automatically
    possible_cols = [c for c in df.columns if c.lower() in ["review", "reviews", "comment", "comments", "feedback", "opinion", "opinions"]]

    if possible_cols:
        review_col = possible_cols[0]
    else:
        review_col = df.columns[0]

    df = df[[review_col]].copy()
    df.columns = ["Review"]
    df["Review"] = df["Review"].astype(str)
    df["Sentiment"] = df["Review"].apply(detect_sentiment)
    return df

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Dashboard Controls")
data_source = st.sidebar.radio(
    "Choose data source",
    ["Demo data", "Upload CSV"]
)

uploaded_file = None
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    st.sidebar.caption("CSV should contain a column with reviews, comments or feedback.")

product_name = st.sidebar.text_input("Product / brand name", value="GlowSkin Cream")
target_group = st.sidebar.text_input("Target audience", value="Women 25–40 interested in skincare")
tone = st.sidebar.selectbox(
    "Tone of voice",
    ["Professional", "Friendly", "Luxury", "Energetic"]
)

# ---------- LOAD DATA ----------
if data_source == "Upload CSV" and uploaded_file is not None:
    try:
        df = normalize_uploaded_file(uploaded_file)
        source_label = "Uploaded CSV"
    except Exception as e:
        st.error(f"Could not read the file. Error: {e}")
        st.stop()
else:
    df = build_demo_df()
    source_label = "Demo dataset"

# ---------- METRICS ----------
total_reviews = len(df)
positive_count = int((df["Sentiment"] == "Positive").sum())
negative_count = int((df["Sentiment"] == "Negative").sum())
neutral_count = int((df["Sentiment"] == "Neutral").sum())

positive_rate = round((positive_count / total_reviews) * 100, 1) if total_reviews else 0
negative_rate = round((negative_count / total_reviews) * 100, 1) if total_reviews else 0

negative_reviews = df[df["Sentiment"] == "Negative"]["Review"]
positive_reviews = df[df["Sentiment"] == "Positive"]["Review"]

top_negative_keywords = extract_keywords(negative_reviews, top_n=6)
top_positive_keywords = extract_keywords(positive_reviews, top_n=6)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🚀 AI Customer Insights Pro</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">Portfolio-level dashboard for customer sentiment analysis and AI-powered marketing ideas • Data source: {source_label}</div>',
    unsafe_allow_html=True
)

# ---------- KPI CARDS ----------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Reviews</div>
        <div class="metric-value">{total_reviews}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Positive Reviews</div>
        <div class="metric-value">{positive_count}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Negative Reviews</div>
        <div class="metric-value">{negative_count}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Positive Rate</div>
        <div class="metric-value">{positive_rate}%</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- CHARTS ----------
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Customer Reviews Explorer")

    sentiment_filter = st.selectbox(
        "Filter by sentiment",
        ["All", "Positive", "Negative", "Neutral"]
    )

    if sentiment_filter == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Sentiment"] == sentiment_filter].copy()

    st.dataframe(filtered_df, use_container_width=True, height=360)
    st.markdown('<div class="small-note">Tip: upload your own CSV to turn this into a real business case study.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Sentiment Overview")

    counts = df["Sentiment"].value_counts().reindex(["Positive", "Negative", "Neutral"], fill_value=0)

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(counts.index, counts.values)
    ax.set_title("Customer Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of reviews")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.bar_label(bars, padding=3)
    st.pyplot(fig)

    st.markdown(f"""
    <div class="small-note">
        Negative rate: <strong>{negative_rate}%</strong> • Positive rate: <strong>{positive_rate}%</strong>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- INSIGHTS ----------
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top Positive Keywords")
    if top_positive_keywords:
        for word, count in top_positive_keywords:
            st.write(f"✅ **{word}** — {count}")
    else:
        st.write("No positive keywords found.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top Customer Pain Points")
    if top_negative_keywords:
        for word, count in top_negative_keywords:
            st.write(f"⚠️ **{word}** — {count}")
    else:
        st.write("No negative keywords found.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- BUSINESS RECOMMENDATIONS ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Business Recommendations")

recommendations = []

if negative_rate >= 40:
    recommendations.append("Customer satisfaction is at risk. Priority should be given to product quality, shipping speed or support issues.")
elif negative_rate >= 20:
    recommendations.append("There are noticeable pain points. A focused improvement campaign could increase retention and reviews.")
else:
    recommendations.append("Customer sentiment is relatively healthy. This is a good moment to scale awareness and social proof.")

if any(word in [w for w, _ in top_negative_keywords] for word in ["slow", "late"]):
    recommendations.append("Shipping and fulfillment appear in negative feedback. Consider improving delivery communication and logistics.")
if any(word in [w for w, _ in top_negative_keywords] for word in ["damaged", "packaging", "broken"]):
    recommendations.append("Packaging quality may be hurting the customer experience. Test stronger packaging and add quality-control checks.")
if any(word in [w for w, _ in top_positive_keywords] for word in ["quality", "beautiful", "great", "excellent"]):
    recommendations.append("Your strongest selling point seems to be product quality. This should be central in ads, product pages and social content.")

for rec in recommendations:
    st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
# ---------- MARKETING GENERATOR ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("AI Marketing Content Generator")

if tone == "Professional":
    post = f"{product_name} delivers dependable quality and a better everyday experience for customers who value effective solutions."
    slogan = f"{product_name} — reliable quality for modern customers."
    campaign = f"Create an educational campaign showing how {product_name} solves common customer problems for {target_group}."
elif tone == "Friendly":
    post = f"Discover {product_name}! A simple way to make your day easier, better and more enjoyable."
    slogan = f"{product_name} — made for real life."
    campaign = f"Launch a social media campaign inviting {target_group} to share their everyday moments with {product_name}."
elif tone == "Luxury":
    post = f"Experience the premium feel of {product_name}, created for people who expect elegance, quality and visible results."
    slogan = f"{product_name} — where quality meets elegance."
    campaign = f"Build a premium lifestyle campaign aimed at {target_group}, focused on exclusivity, visual identity and elevated experience."
else:
    post = f"Ready to level up? {product_name} brings energy, stronger results and a fresh experience to your everyday routine."
    slogan = f"{product_name} — power up your everyday."
    campaign = f"Run a high-energy content series for {target_group}, featuring challenges, creator content and before/after storytelling."

m1, m2 = st.columns(2)

with m1:
    st.markdown("### Social Post")
    st.success(post)

    st.markdown("### Target Audience")
    st.info(target_group)

with m2:
    st.markdown("### Ad Slogan")
    st.success(slogan)

    st.markdown("### Campaign Idea")
    st.warning(campaign)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Built with Python, Streamlit, Pandas and Matplotlib • Portfolio project for AI / Data / Marketing roles")
