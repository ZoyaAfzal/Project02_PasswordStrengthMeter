import streamlit as st
import random
import string

# Set Page Config
st.set_page_config(page_title="🔐 Password Manager", page_icon="🔑", layout="wide")

# Common Weak Passwords
COMMON_PASSWORDS = {"password", "123456", "qwerty", "iloveyou", "admin", "welcome"}

# Initialize Session State
if "saved_passwords" not in st.session_state:
    st.session_state.saved_passwords = []
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""
if "password_history" not in st.session_state:
    st.session_state.password_history = []

# Password Strength Checker
def check_password_strength(password):
    score = 0
    suggestions = []

    if password in COMMON_PASSWORDS:
        return 1, ["❌ Avoid common passwords like 'password123'."]

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("⚠️ Use at least 8 characters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("⚠️ Add at least one uppercase letter.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("⚠️ Add at least one lowercase letter.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("ℹ️ Include at least one number.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        suggestions.append("ℹ️ Use special characters (!@#$%^&*).")

    return score, suggestions

# Password Generator
def generate_password(length, use_digits, use_specials):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_specials:
        characters += string.punctuation
    return "".join(random.choice(characters) for _ in range(length))

# Sidebar
st.sidebar.markdown("<h2 style='color:#00E5FF;'>🔐 Password Tools</h2>", unsafe_allow_html=True)
action = st.sidebar.radio("Choose an option:", ["Check Password Strength", "Generate a Strong Password", "Saved Passwords"])

st.markdown("<h1 style='text-align:center; color:#00E5FF;'>🔐 Secure Password Manager</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

if action == "Check Password Strength":
    st.subheader("🔍 Check Your Password Strength")

    # Ensure password history is initialized
    if "password_history" not in st.session_state:
        st.session_state.password_history = []

    password = st.text_input("Enter Password:", type="password")

    if password:  # Run only if a password is entered
        if password in st.session_state.password_history[:10]:
            st.error("❌ You cannot use the same password from your last 10 password history!")
        else:
            # Add new password to history (limit to 10)
            st.session_state.password_history.insert(0, password)
            st.session_state.password_history = st.session_state.password_history[:10]

            # Check password strength
            score, suggestions = check_password_strength(password)
            score = max(1, min(score, 5))

            # Display strength bar and suggestions
            st.progress(score / 5)
            strength_levels = ["Very Weak ❌", "Weak ⚠️", "Moderate ℹ️", "Strong ✅", "Very Strong 💪"]
            st.markdown(f"<div style='color:#00E5FF;'><h3>💡 {strength_levels[score-1]}</h3></div>", unsafe_allow_html=True)

            if score < 5:
                st.write("### Suggestions:")
                for suggestion in suggestions:
                    st.markdown(f"✅ {suggestion}")

elif action == "Generate a Strong Password":
    st.subheader("🔑 Generate a Secure Password")
    length = st.slider("Password Length:", 8, 20, 12)
    include_numbers = st.checkbox("Include Numbers")
    include_special_chars = st.checkbox("Include Special Characters")

    if st.button("🛠 Generate Password"):
        st.session_state.generated_password = generate_password(length, include_numbers, include_special_chars)

        # Save password history (limit to last 5)
        st.session_state.password_history.insert(0, st.session_state.generated_password)
        st.session_state.password_history = st.session_state.password_history[:5]

        st.success(f"🔑 Your Secure Password: `{st.session_state.generated_password}`")

    # Show history of generated passwords
    if st.session_state.password_history:
        st.subheader("📜 Password History")
        for i, pwd in enumerate(st.session_state.password_history, start=1):
            st.code(f"{i}. {pwd}")

    if st.button("💾 Save Password"):
        if st.session_state.generated_password:
            if st.session_state.generated_password in st.session_state.saved_passwords[-10:]:
                st.error("❌ This password has been used recently! Try generating a new one.")
            else:
                st.session_state.saved_passwords.append(st.session_state.generated_password)
                st.success("✅ Password saved successfully!")
        else:
            st.markdown("""
        <div style='background-color:#00E5FF; color:#000; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>
        ⚠️ No password generated yet!
        </div>
""", unsafe_allow_html=True)

elif action == "Saved Passwords":
    st.subheader("💾 Saved Passwords")
    
    if st.session_state.saved_passwords:
        for idx, password in enumerate(st.session_state.saved_passwords, 1):
            st.code(f"{idx}. {password}")
    else:
        st.markdown("""
    <div style='background-color:#00E5FF; color:#000; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>
        ⚠️ No saved passwords yet.
    </div>
""", unsafe_allow_html=True)

# Footer with profile pic (Use a URL instead of local file)
st.markdown("""
    <div style='text-align:center; font-size:16px; margin-top:20px; color:#00E5FF;'>
        ❤️ Created by <b>Zoya Afzal</b>
    </div>
""", unsafe_allow_html=True)
