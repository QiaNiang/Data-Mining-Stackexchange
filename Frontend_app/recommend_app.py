import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from joblib import load
import numpy as np
import pandas as pd
import json

# ==== Load all models and data ====
ART_DIR = r'E:\Studium\Model'

@st.cache_resource
def load_components():
    model = SentenceTransformer(f'{ART_DIR}/transformer')
    classifiers = load(f'{ART_DIR}/classifiers.joblib')
    mlb_valid = load(f'{ART_DIR}/mlb_valid.joblib')
    with open(f'{ART_DIR}/valid_tag_indices.json') as f:
        valid_tag_indices = json.load(f)
    X = np.load(f'{ART_DIR}/physics_posts_embeddings_.npy')
    df = pd.read_csv(f'{ART_DIR}/physics_post_cleaned_all.csv')
    predicted_tags_all = load(f'{ART_DIR}/predicted_tags_all.joblib')
    return model, classifiers, valid_tag_indices, mlb_valid, X, df, predicted_tags_all

model, classifiers, valid_tag_indices, mlb_valid, X, df, predicted_tags_all = load_components()


# ==== Prediction and Recommendation Functions ====
def predict_tags_single(embedding, classifiers, valid_tag_indices, mlb_valid, top_k=5):
    probs = []
    for idx in valid_tag_indices:
        clf = classifiers[idx]
        prob = clf.predict_proba([embedding])[:, 1][0] if clf else 0.0
        probs.append(prob)
    names = mlb_valid.classes_
    top_idxs = np.argsort(probs)[-top_k:][::-1]
    return set(names[i] for i in top_idxs)

def recommend_for_input(text, model, classifiers, valid_tag_indices, mlb_valid,
                        X_existing, df_existing, predicted_tags_all,
                        top_k_tags=5, top_k_candidates=50, top_n=5, alpha=0.6):
    embedding = model.encode([text])[0]
    predicted_tags = predict_tags_single(embedding, classifiers, valid_tag_indices, mlb_valid, top_k=top_k_tags)
    sims = cosine_similarity([embedding], X_existing)[0]
    inds = np.argpartition(-sims, top_k_candidates)[:top_k_candidates]
    inds = inds[np.argsort(sims[inds])[::-1]]
    res = []
    for i in inds:
        tags_i = predicted_tags_all[i]
        tag_score = len(predicted_tags & tags_i) / (len(predicted_tags) or 1)
        final = alpha * sims[i] + (1 - alpha) * tag_score
        res.append({
            'index': i,
            'sim': float(sims[i]),
            'tag_score': tag_score,
            'final_score': final,
            'tags': df_existing.iloc[i]['Tags'],
            'predicted_tags': list(tags_i),
            'text': df_existing.iloc[i]['CleanBodyNoMath']
        })
    return predicted_tags, sorted(res, key=lambda x: x['final_score'], reverse=True)[:top_n]


# ==== Streamlit UI ====
st.title("🧠 Physics Post Recommender")
st.write("Enter your physics-related question or topic below:")

query = st.text_area("📥 Input your query here:", height=100, placeholder="e.g., apply classical mechanics to motion problems")

if st.button("🔍 Recommend Similar Posts"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing..."):
            pred_tags, results = recommend_for_input(
                text=query,
                model=model,
                classifiers=classifiers,
                valid_tag_indices=valid_tag_indices,
                mlb_valid=mlb_valid,
                X_existing=X,
                df_existing=df,
                predicted_tags_all=predicted_tags_all
            )

        st.markdown(f"### ✅ Predicted Tags: {', '.join(pred_tags)}")
        st.markdown("### 🔗 Top Recommended Posts:")
        for i, r in enumerate(results, 1):
            st.markdown(f"#### {i}. Final Score: `{r['final_score']:.3f}` | Tags: `{r['tags']}`")
            st.write(r['text'][:400] + "...")
