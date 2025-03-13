import streamlit as st
import math
import string
from zxcvbn import zxcvbn

# Function to calculate password entropy
def calculate_entropy(password):
    charsets = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "special": string.punctuation,
    }

    pool_size = sum(len(chars) for name, chars in charsets.items() if any(c in chars for c in password))
    entropy = len(password) * math.log2(pool_size) if pool_size else 0
    return entropy

# Function to check password strength
def check_password_strength(password):
    if not password:
        return "Enter a password to check strength", "⚪", "gray"

    entropy = calculate_entropy(password)
    score_data = zxcvbn(password)
    score = score_data['score']

    strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    colors = ["red", "orange", "yellow", "blue", "green"]
    icons = ["🔴", "🟠", "🟡", "🔵", "🟢"]

    return strength_levels[score], icons[score], colors[score]

# Streamlit UI
st.title("🔐 Password Strength Meter")

password = st.text_input("Enter your password:", type="password")

if password:
    strength, icon, color = check_password_strength(password)
    st.markdown(f"### Strength: {icon} **{strength}**", unsafe_allow_html=True)

    # Display entropy value
    entropy = calculate_entropy(password)
    st.write(f"🔢 **Entropy:** {entropy:.2f} bits (Higher is better)")

    # Suggestions
    if strength in ["Very Weak", "Weak"]:
        st.warning("❌ Your password is too weak! Try using at least 12+ characters with a mix of uppercase, lowercase, numbers, and special symbols.")
    elif strength == "Medium":
        st.info("⚠️ Your password is okay but could be stronger. Consider adding more complexity.")
    else:
        st.success("✅ Your password is strong!")
        # Footer with your name

