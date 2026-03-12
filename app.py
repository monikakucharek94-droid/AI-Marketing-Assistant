import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Customer Insights", page_icon="🚀", layout="wide")

st.title("🚀 AI Customer Insights & Marketing Generator")
st.write("Analyze customer reviews and generate marketing ideas.")

reviews = [
    "This product is amazing",
    "The delivery was very slow",
    "I love this cream",
    "Terrible packaging",
    "Very good quality",
    "Not worth the price"
]

positive_words = ["amazing", "love", "good"]
negative_words = ["slow", "terrible", "not worth"]

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

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Reviews")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Sentiment Summary")
    counts = df["Sentiment"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax)
    st.pyplot(fig)

st.subheader("Generate Marketing Content")
product = st.text_input("Enter product name")

if product:
    st.success("Marketing Post Idea")
    st.write(f"Discover {product} – designed to make your everyday life easier and better.")
    
    st.success("Ad Slogan")
    st.write(f"{product} – quality you can feel.")
    
    st.success("Campaign Idea")
    st.write(f"Create a social media campaign where customers share their experience with {product}.")
