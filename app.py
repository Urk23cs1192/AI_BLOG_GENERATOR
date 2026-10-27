from flask import Flask, render_template, request
import ollama
import json
import os
from datetime import datetime

app = Flask(__name__)

# Ollama model
MODEL = "llama3.2:latest"


# ============================================================
# AI BLOG CONTENT GENERATION
# ============================================================

def generate_all_content(topic, style, tone, word_count, audience):

    prompt = f"""
You are an AI-powered blog content generator.

Create complete blog content using these requirements:

Topic: {topic}
Writing Style: {style}
Tone: {tone}
Word Count: {word_count}
Target Audience: {audience}

Return ONLY valid JSON in exactly this format:

{{
    "intent": "BLOG_GENERATION",
    "title": "A suitable professional blog title",
    "blog": "Complete blog content with introduction, headings, main content and conclusion",
    "summary": "A short 3 to 5 sentence summary",
    "keywords": "keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, keyword8",
    "meta_description": "An attractive SEO-friendly meta description of around 150 characters"
}}

Requirements:

1. The intent must be BLOG_GENERATION.
2. Generate a professional and meaningful title.
3. Generate approximately {word_count} words of blog content.
4. Use clear and simple English.
5. Include Introduction, meaningful sections and Conclusion.
6. Generate a useful summary.
7. Generate 8 to 10 SEO keywords.
8. Generate an SEO-friendly meta description.
9. Do not use Markdown code fences around the JSON.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"].strip()

    # Remove accidental markdown code fences
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        data = json.loads(result)

    except json.JSONDecodeError:

        # Fallback if model does not return perfect JSON
        data = {
            "intent": "BLOG_GENERATION",
            "title": "AI-Generated Blog",
            "blog": result,
            "summary": "AI-generated blog content.",
            "keywords": (
                "Artificial Intelligence, AI, Technology, "
                "Innovation, Digital Transformation"
            ),
            "meta_description": (
                "Learn about this topic through an informative "
                "AI-generated blog."
            )
        }

    return data


# ============================================================
# HOME SCREEN
# ============================================================

@app.route("/")
def home():

    return render_template("home.html")


# ============================================================
# BLOG GENERATOR / USER INPUT SCREEN
# ============================================================

@app.route("/generator")
def generator():

    return render_template("index.html")


# ============================================================
# GENERATE BLOG
# ============================================================

@app.route("/generate", methods=["POST"])
def generate():

    # Get user input
    topic = request.form.get("topic", "").strip()

    style = request.form.get(
        "style",
        "Professional"
    )

    tone = request.form.get(
        "tone",
        "Friendly"
    )

    word_count = request.form.get(
        "word_count",
        "500"
    )

    audience = request.form.get(
        "audience",
        ""
    ).strip()


    # Validate required fields
    if not topic or not audience:

        return render_template(
            "index.html",
            error="Please enter the blog topic and target audience.",
            topic=topic,
            style=style,
            tone=tone,
            word_count=word_count,
            audience=audience
        )


    # Display progress in terminal
    print("\n" + "=" * 60)
    print("AI-POWERED BLOG CONTENT GENERATOR")
    print("=" * 60)

    print("Topic:", topic)
    print("Writing Style:", style)
    print("Tone:", tone)
    print("Word Count:", word_count)
    print("Target Audience:", audience)

    print("-" * 60)
    print("Generating blog content using Llama 3.2...")
    print("-" * 60)


    try:

        # Generate all content
        data = generate_all_content(
            topic,
            style,
            tone,
            word_count,
            audience
        )


        print("Content generated successfully!")

        print("-" * 60)
        print("Intent:", data.get("intent"))
        print("Title:", data.get("title"))
        print("-" * 60)


        # Send generated content to HTML
        return render_template(
            "index.html",

            # User input
            topic=topic,
            style=style,
            tone=tone,
            word_count=word_count,
            audience=audience,

            # AI output
            intent=data.get(
                "intent",
                "BLOG_GENERATION"
            ),

            title=data.get(
                "title",
                "AI Generated Blog"
            ),

            blog=data.get(
                "blog",
                ""
            ),

            summary=data.get(
                "summary",
                ""
            ),

            keywords=data.get(
                "keywords",
                ""
            ),

            meta_description=data.get(
                "meta_description",
                ""
            )
        )


    except Exception as e:

        print("ERROR:", e)

        return render_template(
            "index.html",

            error=f"Error while generating content: {str(e)}",

            topic=topic,
            style=style,
            tone=tone,
            word_count=word_count,
            audience=audience
        )


# ============================================================
# SAVE BLOG
# ============================================================

@app.route("/save", methods=["POST"])
def save_blog():

    # Get generated content from form
    title = request.form.get(
        "title",
        ""
    )

    blog = request.form.get(
        "blog",
        ""
    )

    summary = request.form.get(
        "summary",
        ""
    )

    keywords = request.form.get(
        "keywords",
        ""
    )

    meta_description = request.form.get(
        "meta_description",
        ""
    )


    # Create outputs folder
    os.makedirs(
        "outputs",
        exist_ok=True
    )


    # Generate unique filename
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"blog_{timestamp}.txt"

    filepath = os.path.join(
        "outputs",
        filename
    )


    # Save blog
    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AI-POWERED BLOG CONTENT GENERATOR\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )


        file.write(
            "BLOG TITLE\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            title + "\n\n"
        )


        file.write(
            "BLOG CONTENT\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            blog + "\n\n"
        )


        file.write(
            "SUMMARY\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            summary + "\n\n"
        )


        file.write(
            "SEO KEYWORDS\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            keywords + "\n\n"
        )


        file.write(
            "META DESCRIPTION\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            meta_description + "\n"
        )


    print("\n" + "=" * 60)
    print("BLOG SAVED SUCCESSFULLY!")
    print("=" * 60)
    print("File:", filepath)
    print("=" * 60)


    # Show successful save screen/message
    return render_template(
        "index.html",

        saved=True,

        filename=filename
    )


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
