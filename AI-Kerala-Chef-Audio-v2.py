import streamlit as st
import ollama
from fpdf import FPDF
from gtts import gTTS
import io

# --- Functions for PDF and TTS ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

def text_to_speech(text):
    clean_text = text.replace('#', '').replace('*', '') 
    tts = gTTS(text=clean_text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- UI Layout ---
st.set_page_config(page_title="Kerala AI Chef Pro", page_icon="🥘")
st.title("🌴 Kerala AI Kitchen Assistant")

with st.sidebar:
    st.header("Cooking Preferences")
    dish_type = st.selectbox("Style:", ["Thoran", "Mezhukkupuratti (Fry)", "Curry", "Roast"])
    category = st.radio("Category:", ["Vegetarian", "Chicken", "Fish", "Beef", "Egg"])

# --- Logic to Grey Out/Disable Ingredients ---
# Condition: (Chicken AND Curry) OR (Fish AND Mezhukkupuratti/Fry)
is_locked = (category == "Chicken" and dish_type == "Curry") or \
            (category == "Fish" and dish_type == "Mezhukkupuratti (Fry)")

if is_locked:
    # Set a default value so the LLM knows what to cook even if input is disabled
    default_val = f"{category}"
    st.info(f"💡 Main ingredient locked to **{category}** for this classic combo.")
else:
    default_val = ""

# The 'disabled' parameter handles the "greying out"
ingredients = st.text_input(
    "Enter additional ingredients (optional):", 
    value=default_val,
    placeholder="e.g., Mango, Potato, or Drumstick",
    disabled=is_locked
)

# --- Generate Button ---
if st.button("Generate Recipe"):
    # If locked, use the category as the main ingredient
    search_term = category if is_locked else ingredients
    
    if search_term:
        with st.spinner(f"Preparing your {category} {dish_type}..."):
            prompt = f"Expert Kerala Chef recipe for {category} {dish_type} using {search_term}. Focus on authentic spices."
            response = ollama.chat(model="llama3.2", messages=[{'role': 'user', 'content': prompt}])
            st.session_state['recipe'] = response['message']['content']
    else:
        st.warning("Please enter an ingredient!")

# --- Display Results ---
if 'recipe' in st.session_state:
    recipe = st.session_state['recipe']
    
    st.subheader("🔊 Audio Instructions")
    st.audio(text_to_speech(recipe), format='audio/mp3')
    
    st.markdown("---")
    st.markdown(recipe)
    
    # PDF Download
    st.download_button("📥 Save Recipe (PDF)", create_pdf(recipe), "kerala_recipe.pdf", "application/pdf")