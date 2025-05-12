from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

def seo_refine_blog(blog_content):
    prompt = f"""
You are an expert SEO strategist and content editor.

Your job is to optimize the following blog post for SEO while keeping the original meaning, tone, and structure intact.

Apply the following improvements:
- Rewrite the title to be more compelling and keyword-rich
- Add a strong, engaging introduction with a clear hook
- Break content into logical sections with clear, keyword-focused H2 headings
- Use short paragraphs and bullet points to enhance readability
- Naturally insert relevant keywords, LSI terms, and long-tail phrases
- Improve flow, grammar, and clarity without changing key points
- End with a strong conclusion and a call-to-action
- If missing, add suggested SEO meta title, description, and keywords at the bottom

Keep the content professional yet friendly. Don’t remove any important message or personal voice.

---BLOG START---
{blog_content}
---BLOG END---

Return only the fully optimized blog post.
"""
    model = genai.GenerativeModel("gemini-2.0-flash ")  # You can use "flash" if preferred, but "pro" is stronger
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
