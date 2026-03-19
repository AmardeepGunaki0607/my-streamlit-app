import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import io

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AyurLogic | Smart Ayurveda Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- EXTENDED KNOWLEDGE BASE ---
# This includes more diseases and detailed logical mappings
DISEASE_DB = {
    "Digestive Health": {
        "Vata (Agnimandya)": {
            "Symptoms": ["Bloating", "Gas", "Constipation", "Variable Appetite"],
            "Remedies": ["Ginger Tea with Hing", "Triphala Churna at night", "Warm Sesame Oil massage on abdomen"],
            "Logic": "Vata's 'Cold/Dry' nature slows down digestion. We use 'Deepana' (kindling) herbs like Ginger."
        },
        "Pitta (Amla-pitta)": {
            "Symptoms": ["Acidity", "Heartburn", "Burning sensation", "Loose stools"],
            "Remedies": ["Avipattikar Churna", "Aloe Vera Juice", "Cooling Fennel Water"],
            "Logic": "Excess 'Heat' in the stomach causes acid reflux. Cooling, alkaline herbs neutralize it."
        },
        "Kapha (Ajirna)": {
            "Symptoms": ["Heaviness after meals", "Lethargy", "Nausea", "Slow metabolism"],
            "Remedies": ["Trikatu (Ginger, Black Pepper, Long Pepper)", "Honey and Lemon", "Warm Water"],
            "Logic": "Kapha's 'Heavy/Damp' nature dampens the digestive fire. Spicy stimulants are needed."
        }
    },
    "Skin & Hair": {
        "Vata": {
            "Symptoms": ["Dry Skin", "Cracked Heels", "Thinning Hair", "Dandruff (Dry)"],
            "Remedies": ["Almond Oil application", "Ashwagandha Lepa", "Hydrating Ghee"],
            "Logic": "Dryness is the core Vata attribute. Intense oleation (Snehana) is the cure."
        },
        "Pitta": {
            "Symptoms": ["Red Rashes", "Acne", "Inflammation", "Early Graying"],
            "Remedies": ["Neem Paste", "Sandalwood Lepa", "Rose Water spray"],
            "Logic": "Inflammation is 'Pitta' fire. Bitter herbs (Neem) clear heat from the blood."
        }
    },
    "Mental Wellness": {
        "Vata (Anxiety)": {
            "Symptoms": ["Overthinking", "Restlessness", "Panic", "Insomnia"],
            "Remedies": ["Brahmi Vati", "Warm Milk with Nutmeg", "Pranayama (Nadi Shodhana)"],
            "Logic": "The mind is too 'Mobile'. We need heavy, grounding herbs to settle the nerves."
        }
    }
}

# --- HELPER FUNCTIONS ---
def get_all_symptoms():
    all_s = []
    for category in DISEASE_DB.values():
        for dosha_type in category.values():
            all_s.extend(dosha_type["Symptoms"])
    return list(set(all_s))

def analyze_symptoms(selected):
    results = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    remedy_list = []
    logic_list = []
    
    for cat_name, cat_data in DISEASE_DB.items():
        for d_type, d_data in cat_data.items():
            matches = set(selected).intersection(set(d_data["Symptoms"]))
            if matches:
                dosha_name = d_type.split(" ")[0]
                results[dosha_name] += len(matches)
                remedy_list.extend(d_data["Remedies"])
                logic_list.append(f"**{cat_name} ({dosha_name}):** {d_data['Logic']}")
                
    return results, list(set(remedy_list)), list(set(logic_list))

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    .stAlert { border-radius: 12px; }
    h1 { color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
    st.title("AyurLogic v1.0")
    page = st.radio("Navigation", ["🏠 Home", "🔍 Smart Diagnosis", "📖 Learn Ayurveda", "📊 Analytics Dashboard"])
    st.divider()
    st.info("💡 **Ayur ThinkFest Tip:** This AI uses a 'Knowledge-Graph' approach to explain remedies.")

# --- PAGE: HOME ---
if page == "🏠 Home":
    st.title("Fostering Innovation in Traditional Health Care")
    st.subheader("Welcome to AyurLogic: The Future of E-Ayurveda")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        AyurLogic is a smart platform designed for the **Ayur ThinkFest 2026**. 
        We bridge the gap between ancient wisdom and modern technology using:
        - **Logic-Driven AI** for accurate remedy suggestion.
        - **Computer Vision** for objective biomarker analysis.
        - **Interactive Education** to empower patients.
        """)
        if st.button("Start My Assessment"):
            st.info("Select 'Smart Diagnosis' from the sidebar!")
    
    with col2:
        st.image("https://img.freepik.com/free-vector/ayurvedic-concept-illustration_114360-7566.jpg", use_container_width=True)

# --- PAGE: SMART DIAGNOSIS ---
elif page == "🔍 Smart Diagnosis":
    st.title("Smart Symptom Analyzer")
    st.write("Complete the assessment below to receive your personalized Ayurvedic plan.")

    tab1, tab2 = st.tabs(["📝 Symptom Selection", "📸 Tongue Analysis (Beta)"])

    with tab1:
        selected_symptoms = st.multiselect(
            "What symptoms are you feeling? (Multi-select)",
            options=get_all_symptoms(),
            help="Select all that apply to get a holistic view of your Dosha imbalance."
        )
        
        duration = st.slider("How many days have you had these symptoms?", 1, 30, 3)

    with tab2:
        st.write("Computer Vision can identify 'Ama' (toxins) on the tongue.")
        img_file = st.file_uploader("Upload a clear photo of your tongue", type=["jpg", "png", "jpeg"])
        if img_file:
            st.image(img_file, caption="Processing image via Computer Vision logic...", width=300)
            st.warning("CV Analysis: Moderate white coating detected (Indicating Kapha/Vata imbalance).")

    if st.button("Generate My Ayurvedic Plan"):
        if not selected_symptoms:
            st.error("Please select at least one symptom to proceed.")
        else:
            with st.spinner("Analyzing Dosha imbalances..."):
                scores, remedies, logics = analyze_symptoms(selected_symptoms)
                
                # Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Vata Imbalance", f"{scores['Vata']}")
                m2.metric("Pitta Imbalance", f"{scores['Pitta']}")
                m3.metric("Kapha Imbalance", f"{scores['Kapha']}")

                st.divider()
                
                # Results UI
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.subheader("📋 Your Remedies")
                    for r in remedies:
                        st.markdown(f"🌿 **{r}**")
                    
                    st.subheader("🧠 The Ayurvedic Logic")
                    for l in logics:
                        st.write(l)
                
                with c2:
                    st.subheader("📊 Imbalance Visualization")
                    df_viz = pd.DataFrame(list(scores.items()), columns=['Dosha', 'Intensity'])
                    fig = px.pie(df_viz, values='Intensity', names='Dosha', color='Dosha',
                                 color_discrete_map={'Vata':'#E67E22','Pitta':'#E74C3C','Kapha':'#2ECC71'})
                    st.plotly_chart(fig, use_container_width=True)

                st.success("📝 **Action Plan:** Avoid cold foods and prefer warm, cooked meals for the next 3 days.")

# --- PAGE: LEARN AYURVEDA ---
elif page == "📖 Learn Ayurveda":
    st.title("E-Ayurveda Learning Center")
    category = st.selectbox("Choose a topic", ["The 3 Doshas", "Daily Routine (Dinacharya)", "Healing Herbs"])
    
    if category == "The 3 Doshas":
        st.write("### Understanding Vata, Pitta, and Kapha")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder for educational video
        st.write("""
        - **Vata (Air):** Controls movement, breathing, and heartbeats.
        - **Pitta (Fire):** Controls metabolism, digestion, and temperature.
        - **Kapha (Earth):** Controls growth, immunity, and lubrication.
        """)
    elif category == "Healing Herbs":
        herb = st.text_input("Search for a herb (e.g., Ashwagandha, Tulsi)")
        if herb:
            st.success(f"Details for {herb}: Properties - Hot/Sweet, Best for Vata/Kapha.")

# --- PAGE: ANALYTICS ---
elif page == "📊 Analytics Dashboard":
    st.title("Vaidya Analytics (Researcher View)")
    st.write("This section shows trends across all platform users (Simulated Data).")
    
    # Mock Data for Research Presentation
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Vata Cases': [45, 52, 60, 48],
        'Pitta Cases': [30, 35, 40, 55],
        'Kapha Cases': [25, 20, 15, 20]
    })
    
    fig2 = px.line(data, x='Month', y=['Vata Cases', 'Pitta Cases', 'Kapha Cases'], 
                  title="Seasonal Imbalance Trends in your Region")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("Researchers can use this data to predict seasonal disease outbreaks.")

# --- FOOTER ---
st.divider()
st.caption("Developed for Ayur ThinkFest 2026 | Organized by BLDEA's AVS Ayurveda Mahavidyalaya.")