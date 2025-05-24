import pandas as pd

# Load both files
sentiment_df = pd.read_csv("../data/UsersWithSentiment.csv")
country_df = pd.read_csv("../data/UsersWithCountry.csv")

# Keep only needed columns from sentiment
sentiment_df = sentiment_df[["Id", "SentimentLabel", "SentimentScore"]]

# Merge on Id
merged = country_df.merge(sentiment_df, on="Id", how="left")

# Add SentimentValue column
label_to_score = {"negative": -1, "neutral": 0, "positive": 1}
merged["SentimentValue"] = merged["SentimentLabel"].map(label_to_score)

# Save merged file
merged.to_csv("../data/UsersWithSentimentAndCountry.csv", index=False)
