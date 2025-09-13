import streamlit as st
import requests

# ---------------------------
# Config
# ---------------------------
BACKEND_URL = "http://localhost:8000"  # FastAPI backend
st.set_page_config(page_title="AI Email Generator", layout="wide")

# ---------------------------
# CSS for Static Centered Layout
# ---------------------------
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .block-container {
            max-width: 700px;
            margin: auto;
            padding: 2rem;
            border-radius: 12px;
            background-color: #2a2a2a;
            box-shadow: 0 4px 10px rgba(0,0,0,0.6);
        }
        button, .stButton button {
            background-color: #3a3a3a;
            color: white;
            border-radius: 8px;
        }
        </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Title
# ---------------------------
st.markdown(
    "<h2 style='text-align:center;'>AI Email Generator</h2>",
    unsafe_allow_html=True,
)

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2 = st.tabs(["✉️ Generate Email", "📜 History"])

# ---------------------------
# Tab 1: Generate Email
# ---------------------------
with tab1:
    name = st.text_input("Your Name")
    recipient = st.text_input("Recipient Email")
    industry = st.text_input("Industry", placeholder="e.g., SaaS, Finance, Retail")
    role = st.text_input("Role", placeholder="e.g., CTO, HR Manager")
    pain_point = st.text_area("Pain Point", placeholder="e.g., struggling with infra costs")

    tone = st.selectbox("Tone", ["Formal", "Friendly", "Persuasive"])
    template = st.selectbox("Template", ["Cold Outreach", "Follow-up", "Networking", "Sales Pitch"])

    if st.button("✨ Generate Email"):
        payload = {
            "recipient": recipient,
            "industry": industry,
            "role": role,
            "pain_point": pain_point,
            "tone": tone,
            "template": template,
        }

        try:
            res = requests.post(f"{BACKEND_URL}/generate-email", json=payload)
            if res.status_code == 200:
                generated_email = res.json().get("generated_email")
                st.subheader("📩 Generated Email")
                st.code(generated_email, language="markdown")

                if st.button("💾 Save this email"):
                    save_res = requests.post(
                        f"{BACKEND_URL}/save-email", json={**payload, "generated_email": generated_email}
                    )
                    if save_res.status_code == 200:
                        st.success("✅ Email saved to history!")
                    else:
                        st.error("❌ Failed to save email")
            else:
                st.error("❌ Failed to generate email")
        except Exception as e:
            st.error(f"Backend error: {e}")

# ---------------------------
# Tab 2: History
# ---------------------------
with tab2:
    user_email = st.text_input("Enter your email to fetch history")

    if st.button("🔍 Fetch History"):
        try:
            res = requests.get(f"{BACKEND_URL}/history", params={"user": user_email})
            if res.status_code == 200:
                history = res.json()
                if history:
                    for item in history:
                        st.markdown(f"**To:** {item['recipient']}")
                        st.code(item['generated_email'], language="markdown")
                        st.caption(f"🕒 {item['created_at']}")
                        st.divider()
                else:
                    st.info("No emails found in history.")
            else:
                st.error("❌ Failed to fetch history")
        except Exception as e:
            st.error(f"Backend error: {e}")
