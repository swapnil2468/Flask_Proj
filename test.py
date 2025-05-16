import streamlit as st
import requests

st.set_page_config(page_title="AI Blog Optimizer", layout="wide")

st.title("🧠 AI Blog Optimizer")
st.write("Paste your raw blog content below and get an SEO-optimized HTML version.")

# Text area for blog input
blog_input = st.text_area("✍️ Enter your blog content", height=300)

# On button click
if st.button("🚀 Optimize Blog"):
    if not blog_input.strip():
        st.warning("Please enter some blog content.")
    else:
        with st.spinner("Contacting Flask API..."):
            try:
                api_url = "https://flask-proj-qhsz.onrender.com/optimize-blog"
                res = requests.post(api_url, json={"blog": blog_input})
                res.raise_for_status()
                result = res.json()

                optimized_html = result.get("optimized_blog", "")
                st.success("✅ Optimization Successful!")

                st.subheader("🔍 Optimized HTML Code")
                st.code(optimized_html, language='html')

                st.subheader("📄 Preview Output")
                st.components.v1.html(
                    f"""
                    <div style="background-color: white; color: black; padding: 2rem; border-radius: 10px;">
                        {optimized_html}
                    </div>
                    """,
                    height=800,
                    scrolling=True
                )


            except Exception as e:
                st.error(f"❌ API call failed: {e}")
