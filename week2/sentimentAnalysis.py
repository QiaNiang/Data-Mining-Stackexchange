import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
import argparse
import os

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["sample", "full"], default="sample", help="Run mode")
args = parser.parse_args()

# Load model and tokenizer
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label map
label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

# Load user data
users = pd.read_csv("../data/Users.csv")

# Load or initialize sentiment data
sentiment_file = "../data/UsersWithSentiment.csv"
if os.path.exists(sentiment_file):
    users_with_sentiment = pd.read_csv(sentiment_file)
else:
    users_with_sentiment = users.copy()
    users_with_sentiment["SentimentLabel"] = pd.NA
    users_with_sentiment["SentimentScore"] = pd.NA

# Sample mode
if args.mode == "sample":
    mask = users_with_sentiment["AboutMe"].notna() & (users_with_sentiment["AboutMe"].str.strip() != "")
    sample_users = users_with_sentiment[mask].sample(n=300, random_state=42).copy()
    texts = sample_users["AboutMe"].str.slice(0, 512).tolist()
    labels = []
    scores = []

    for i in tqdm(range(0, len(texts), 100), desc="Progress"):
        batch = texts[i:i+100]
        results = sentiment_model(batch)
        for r in results:
            labels.append(label_map[r["label"]])
            scores.append(r["score"])

    sample_users["SentimentLabel"] = labels
    sample_users["SentimentScore"] = scores
    users_with_sentiment.update(sample_users[["Id", "SentimentLabel", "SentimentScore"]])
    users_with_sentiment.to_csv(sentiment_file, index=False)
    print(f"Saved 300 sampled users with sentiment to {sentiment_file}")
    exit()

# Full mode: process in batches until done or interrupted
try:
    while True:
        mask = users_with_sentiment["SentimentScore"].isna() & users_with_sentiment["AboutMe"].notna() & (users_with_sentiment["AboutMe"].str.strip() != "")
        valid_users = users_with_sentiment[mask].head(1000).copy()

        if valid_users.empty:
            print("All users already processed. Nothing to do.")
            break

        print(f"Processing {len(valid_users)} users...")

        texts = valid_users["AboutMe"].apply(lambda x: tokenizer.decode(tokenizer(x, truncation=True, max_length=512)["input_ids"])).tolist()
        labels = []
        scores = []

        for i in tqdm(range(0, len(texts), 100), desc="Progress"):
            batch = texts[i:i+100]
            results = sentiment_model(batch)
            for r in results:
                labels.append(label_map[r["label"]])
                scores.append(r["score"])

        valid_users = valid_users.iloc[:len(labels)].copy()
        valid_users["SentimentLabel"] = labels
        valid_users["SentimentScore"] = scores

        users_with_sentiment.update(valid_users[["Id", "SentimentLabel", "SentimentScore"]])
        users_with_sentiment.to_csv(sentiment_file, index=False)
        print(f"Saved {len(valid_users)} users to {sentiment_file}\n")

except KeyboardInterrupt:
    print("Interrupted. Saving partial progress...")
    users_with_sentiment.to_csv(sentiment_file, index=False)
    print("Progress saved.")
