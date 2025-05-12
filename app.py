from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

def seo_refine_blog(blog_content):
    prompt = f"""
You are an expert SEO strategist and blog editor.

Refine the blog below to make it SEO-optimized:
- Keep the meaning and tone intact.
- Improve keywords, structure, and readability.
- Don't remove important info.

---BLOG---
{blog_content}
---END BLOG---

Return the optimized blog.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

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
