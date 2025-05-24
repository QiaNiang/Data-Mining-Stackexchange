import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Load the comments CSV
df = pd.read_csv("Comments.csv")  # Replace with your actual path
df = df[df['Text'].notna()].copy()

# Load sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Label mapping from model labels to readable ones
label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

# Prepare text list
texts = df["Text"].astype(str).tolist()

# Run sentiment analysis in batches
labels = []
scores = []

for i in tqdm(range(0, len(texts), 100), desc="Processing"):
    batch = texts[i:i+100]
    results = sentiment_model(batch, truncation=True, max_length=512)
    for r in results:
        labels.append(label_map[r["label"]])
        scores.append(r["score"])

# Add results to DataFrame
df["SentimentLabel"] = labels
df["SentimentScore"] = scores

# Optional: map sentiment to numeric value
df["SentimentValue"] = df["SentimentLabel"].map({
    "negative": -1,
    "neutral": 0,
    "positive": 1
})

# Save updated CSV
df.to_csv("CommentsWithSentiment.csv", index=False)
