import gradio as gr

# Simulated model logic (replace with your actual model later)
def recommend_tags_and_posts(text):
    if "deep learning" in text.lower():
        tags = ["deep-learning", "neural-networks"]
        posts = [
            {"title": "5 Steps to Start with Deep Learning", "summary": "This post provides practical steps for getting started with deep learning."},
            {"title": "Choosing the Right Neural Network Architecture", "summary": "A discussion on different neural network types and when to use them."}
        ]
    else:
        tags = ["machine-learning", "NLP"]
        posts = [
            {"title": "How to Perform Text Classification", "summary": "This article explains the workflow and model options for text classification."},
            {"title": "Basics of Recommendation Systems", "summary": "An introduction to collaborative filtering and content-based recommendations."}
        ]

    tag_output = ", ".join(tags)
    post_output = "\n\n".join([f"🔹 **{p['title']}**\n{p['summary']}" for p in posts])
    return tag_output, post_output

# Gradio interface
demo = gr.Interface(
    fn=recommend_tags_and_posts,
    inputs=gr.Textbox(lines=6, label="Enter your post content"),
    outputs=[
        gr.Text(label="Recommended Tags"),
        gr.Markdown(label="Recommended Related Posts")
    ],
    title="🧠 Post Recommendation Demo",
    description="Enter a post, and the system will suggest relevant tags and related posts."
)

demo.launch()