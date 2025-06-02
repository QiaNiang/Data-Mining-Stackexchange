import pandas as pd

# ───────────────────────────────────────────────
# 1. File paths
# ───────────────────────────────────────────────
users_path    = "/Users/adilshamji/Documents/25-Data-mining-lab/Data-Mining-Stackexchange/data/UsersWithSentimentAndCountry.csv"
comments_path = "/Users/adilshamji/Documents/25-Data-mining-lab/Data-Mining-Stackexchange/data/Comments.csv"
posts_path    = "/Users/adilshamji/Documents/25-Data-mining-lab/Data-Mining-Stackexchange/data/Posts_with_sentiment.csv"

# ───────────────────────────────────────────────
# 2. Load and rename columns before merge
# ───────────────────────────────────────────────

# USERS
users_df = pd.read_csv(users_path, dtype={"Id": str}).rename(columns={
    "Id": "UserId",
    "Reputation": "users.Reputation",
    "CreationDate": "users.CreationDate",
    "DisplayName": "users.DisplayName",
    "LastAccessDate": "users.LastAccessDate",
    "WebsiteUrl": "users.WebsiteUrl",
    "Location": "users.Location",
    "AboutMe": "users.AboutMe",
    "Views": "users.Views",
    "UpVotes": "users.UpVotes",
    "DownVotes": "users.DownVotes",
    "AccountId": "users.AccountId",
    "LocationCountry": "users.Country",
    "SentimentLabel": "users.SentimentLabel",
    "SentimentScore": "users.SentimentScore",
    "SentimentValue": "users.SentimentValue"
})

# COMMENTS
comments_df = pd.read_csv(comments_path, dtype={"UserId": str, "PostId": str}).rename(columns={
    "Id": "CommentId",
    "PostId": "PostId",
    "Score": "comments.Score",
    "Text": "comments.Text",
    "CreationDate": "comments.CreationDate",
    "UserId": "UserId",
    "UserDisplayName": "comments.UserDisplayName"
})

# Remove comments with missing users
comments_df = comments_df[comments_df["UserId"].notna()]

# POSTS
posts_df = pd.read_csv(posts_path, dtype={"Id": str}).rename(columns={
    "Id": "PostId",
    "PostTypeId": "posts.PostTypeId",
    "AcceptedAnswerId": "posts.AcceptedAnswerId",
    "CreationDate": "posts.CreationDate",
    "Score": "posts.Score",
    "ViewCount": "posts.ViewCount",
    "Body": "posts.Body",
    "OwnerUserId": "posts.OwnerUserId",
    "LastEditorUserId": "posts.LastEditorUserId",
    "LastEditDate": "posts.LastEditDate",
    "LastActivityDate": "posts.LastActivityDate",
    "Title": "posts.Title",
    "Tags": "posts.Tags",
    "AnswerCount": "posts.AnswerCount",
    "CommentCount": "posts.CommentCount",
    "ContentLicense": "posts.ContentLicense",
    "ParentId": "posts.ParentId",
    "OwnerDisplayName": "posts.OwnerDisplayName",
    "ClosedDate": "posts.ClosedDate",
    "LastEditorDisplayName": "posts.LastEditorDisplayName",
    "CommunityOwnedDate": "posts.CommunityOwnedDate",
    "FavoriteCount": "posts.FavoriteCount",
    "CleanBodyNoMath": "posts.CleanBodyNoMath",
    "SentimentScore": "posts.SentimentScore",
    "SentimentLabel": "posts.SentimentLabel"
})

# ───────────────────────────────────────────────
# 3. Merge posts ←→ comments
# ───────────────────────────────────────────────
posts_comments = posts_df.merge(
    comments_df,
    on="PostId",
    how="left",
    suffixes=("", "_comment")
)

# ───────────────────────────────────────────────
# 4. Merge in users
# ───────────────────────────────────────────────
posts_comments_users = posts_comments.merge(
    users_df,
    on="UserId",
    how="left",
    suffixes=("", "_user")
)

# ───────────────────────────────────────────────
# 5. Optional sanity filter: keep rows with post OR comment
# ───────────────────────────────────────────────
has_post = posts_comments_users["posts.Body"].fillna("").str.strip() != ""
has_comment = posts_comments_users["comments.Text"].fillna("").str.strip() != ""
final_df = posts_comments_users[has_post | has_comment]

# ───────────────────────────────────────────────
# 6. Save result
# ───────────────────────────────────────────────
output_path = "/Users/adilshamji/Documents/25-Data-mining-lab/Data-Mining-Stackexchange/data/posts_with_comments_and_users.csv"
final_df.to_csv(output_path, index=False)
print(f"✅ Final merged file saved to: {output_path}")
