import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CoffeeBot Assistant",
    page_icon="☕",
    layout="centered"
)

# =========================================================
# KNOWLEDGE BASE
# =========================================================
COFFEE_MENU = """
Coffee Shop Menu:
1. Espresso
   - Strong, concentrated coffee shot
   - Best for: strong coffee lovers

2. Americano
   - Espresso + hot water
   - Best for: lighter but bold taste

3. Cappuccino
   - Espresso + steamed milk + foam
   - Best for: creamy balanced taste

4. Latte
   - Espresso + more steamed milk
   - Best for: smooth and mild coffee

5. Mocha
   - Latte + chocolate
   - Best for: sweet coffee lovers

6. Macchiato
   - Espresso with a small amount of foam
   - Best for: bold with slight creaminess

7. Cold Brew
   - Cold steeped coffee
   - Best for: smooth, low acidity

Available Sizes:
- Small (250ml)
- Medium (350ml)
- Large (500ml)

Add-ons:
- Extra shot
- Oat milk
- Almond milk
- Caramel syrup
- Hazelnut syrup

Recommendation Guide:
- Strong coffee → Espresso / Americano
- Creamy → Latte / Cappuccino
- Sweet → Mocha / Caramel Latte
- Low acidity → Cold Brew
"""

SYSTEM_PROMPT = f"""
You are CoffeeBot, a professional AI coffee shop customer service assistant.

Rules:
1. Only answer questions related to coffee, drinks, menu, recommendations, and coffee knowledge.
2. Use this menu as primary knowledge:
{COFFEE_MENU}
3. Recommend the closest suitable menu item based on user preferences, even if the exact wording is not in the menu.
4. For low caffeine requests, suggest smoother or perceived lighter options such as Cold Brew or milk-based drinks, while clearly noting caffeine levels can vary.
5. If users are unsure, ask about their taste preference (sweet, creamy, strong, low acidity).
6. Be friendly, concise, and helpful like an expert barista.
7. If user asks outside coffee topics, politely redirect them.
8. Do not say an option is unavailable unless absolutely none of the menu items fit.
"""

# =========================================================
# HEADER
# =========================================================
st.title("☕ CoffeeBot Assistant")
st.subheader("Your AI Coffee Shop Customer Service")
st.caption("Ask me about menu, coffee recommendations, flavors, or brewing tips!")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")

    tone = st.selectbox(
        "Choose chatbot tone",
        ["Friendly", "Formal", "Casual"]
    )

    if st.button("Reset Chat"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### Example Questions:")
    st.markdown("- I like sweet coffee")
    st.markdown("- What’s the difference between latte and cappuccino?")
    st.markdown("- Recommend low caffeine coffee")
    st.markdown("- Which coffee is creamy?")

# =========================================================
# TONE ADJUSTMENT
# =========================================================
tone_instruction = {
    "Friendly": "Respond warmly and helpfully.",
    "Formal": "Respond professionally and formally.",
    "Casual": "Respond casually and conversationally."
}

# =========================================================
# API VALIDATION
# =========================================================
if not api_key:
    st.info("Please enter your Gemini API key in the sidebar.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Invalid API Key: {e}")
    st.stop()

# =========================================================
# SESSION MEMORY
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I’m CoffeeBot ☕ What kind of coffee do you like? Strong, sweet, creamy, or something smooth?"
        }
    ]

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# USER INPUT
# =========================================================
user_input = st.chat_input("Ask anything about coffee...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    full_prompt = f"""
{SYSTEM_PROMPT}

Additional tone:
{tone_instruction[tone]}

Customer Question:
{user_input}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        bot_reply = response.text

    except Exception as e:
        bot_reply = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })