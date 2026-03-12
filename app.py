import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Customer Insights Dashboard",
    page_icon="🚀",
    layout="wide"
)

reviews = [
    "This product is amazing",
    "The delivery was very slow",
    "I love this cream",
    "Terrible packaging",
    "Very good quality",
    "Not worth the price",
    "Excellent results after one week",
    "Customer service was disappointing",
    "Beautiful design and great quality",
    "The package arrived damaged"
]

positive_words = ["amazing", "love", "good", "excellent", "great", "beautiful"]
negative_words = ["slow", "terrible", "not worth", "disappointing", "damaged"]

results = []
for review in reviews:
    text = review.lower()
    if any(word in text for word in positive_words):
        sentiment = "Positive"
    elif any(word in text for word in negative_words):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    results.append({"Review": review, "Sentiment": sentiment})

df = pd.DataFrame(results)

positive_count = (df["Sentiment"] == "Positive").sum()
negative_count = (df["Sentiment"] == "Negative").sum()
neutral_count = (df["Sentiment"] == "Neutral").sum()
total_reviews = len(df)

st.title("🚀 AI Customer Insights Dashboard")
st.caption("Analyze customer reviews and generate marketing ideas for a product or service.")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reviews", total_reviews)
col2.metric("Positive", positive_count)
col3.metric("Negative", negative_count)
col4.metric("Neutral", neutral_count)

st.markdown("## Customer Review Analysis")

left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("Review Table")
    sentiment_filter = st.selectbox(
        "Filter by sentiment",
        ["All", "Positive", "Negative", "Neutral"]
    )

    if sentiment_filter == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Sentiment"] == sentiment_filter]

    st.dataframe(filtered_df, use_container_width=True)

with right_col:
    st.subheader("Sentiment Summary")
    counts = df["Sentiment"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of reviews")
    ax.set_title("Customer Sentiment Overview")
    st.pyplot(fig)

st.markdown("---")
st.markdown("## AI Marketing Content Generator")

product = st.text_input("Enter product or service name")
target_group = st.text_input("Enter target audience", placeholder="e.g. women 25-40, skincare lovers")

tone = st.selectbox(
    "Choose tone of voice",
    ["Professional", "Friendly", "Luxury", "Energetic"]
)

if product:
    st.markdown("### Generated Marketing Content")

    if tone == "Professional":
        post = f"{product} is designed to deliver reliable quality and a better everyday experience for customers."
        slogan = f"{product} – smart quality you can trust."
        campaign = f"Launch an educational campaign showing how {product} solves real customer problems."
    elif tone == "Friendly":
        post = f"Discover {product}! A simple way to make your day easier, better and more enjoyable."
        slogan = f"{product} – made for real life."
        campaign = f"Encourage customers to share their favorite moments with {product} on social media."
    elif tone == "Luxury":
        post = f"Experience the elegance of {product}, created for people who expect premium quality and exceptional results."
        slogan = f"{product} – where quality meets elegance."
        campaign = f"Build a premium campaign focused on style, exclusivity and customer experience around {product}."
    else:
        post = f"Ready to level up? {product} brings fresh energy, better results and a new standard of quality."
        slogan = f"{product} – power up your everyday."
        campaign = f"Create a high-energy social media challenge that promotes {product} with user-generated content."

    if target_group:
        audience_line = f"Recommended audience: {target_group}"
    else:
        audience_line = "Recommended audience: general consumer audience"

    box1, box2 = st.columns(2)

    with box1:
        st.success("Instagram / LinkedIn Post")
        st.write(post)

        st.info("Recommended Audience")
        st.write(audience_line)

    with box2:
        st.success("Advertising Slogan")
        st.write(slogan)

        st.warning("Campaign Idea")
        st.write(campaign)

st.markdown("---")
st.caption("Built with Python, Streamlit, Pandas and Matplotlib.")
