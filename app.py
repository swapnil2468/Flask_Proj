from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)  # 👈 enable CORS for all routes

def seo_refine_blog(blog_content):
    prompt = f"""
You are an expert SEO blog writer and web editor.
Your job is to fully optimize the following blog post for SEO while keeping its tone, voice, and structure.

Please follow these exact rules:
- Do NOT include any introductory messages or explanations.
- Return ONLY the optimized blog content in clean, SEO-ready HTML format.
- Use:
  - <h1> for the main title
  - <h2> for subheadings
  - <p> for paragraphs
  - <ul><li> for bullet points

Here is the blog:
---BLOG START---
{blog_content}
---BLOG END---

Return ONLY the HTML-formatted, optimized blog content. Do NOT add meta titles, descriptions, or keywords.
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/optimize-blog', methods=['POST'])
def optimize_blog():
    data = request.get_json()
    blog = data.get("blog")
    if not blog:
        return jsonify({"error": "No blog content provided"}), 400
    try:
        optimized_blog = seo_refine_blog(blog)
        return jsonify({"optimized_blog": optimized_blog})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
