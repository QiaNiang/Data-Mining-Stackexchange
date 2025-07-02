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

# Gradio interface with vertical layout
with gr.Blocks() as demo:
    gr.Markdown("## Post Recommendation Demo")
    gr.Markdown("Enter a post, and the system will suggest relevant tags and related posts.")
    
    with gr.Row():
        input_box = gr.Textbox(lines=6, label="Enter your post content")

    submit_button = gr.Button("Analyze")
    tag_output = gr.Text(label="Recommended Tags")
    post_output = gr.Markdown(label="Recommended Related Posts")

    submit_button.click(
        fn=recommend_tags_and_posts,
        inputs=input_box,
        outputs=[tag_output, post_output]
    )

demo.launch()