import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Ayurveda AI", layout="centered")

st.title("🌿 E-Ayurveda AI System")
st.subheader("Explainable AI + Dosha Analytics")

menu = st.sidebar.selectbox("Choose Mode", ["Home", "Diagnose", "Learn Ayurveda"])

# ---------------- HOME ----------------
if menu == "Home":
    st.write("AI-powered Ayurveda platform")
    st.write("✔ Learn Doshas")
    st.write("✔ Diagnose symptoms")
    st.write("✔ Get personalized remedies")

# ---------------- DIAGNOSE ----------------
elif menu == "Diagnose":
    st.header("🩺 Enter Your Symptoms")

    symptom = st.text_area("Example: stress, acidity, fatigue")

    if st.button("Analyze"):

        vata_keywords = ["stress", "anxiety", "dry", "insomnia"]
        pitta_keywords = ["heat", "acidity", "anger", "burning"]
        kapha_keywords = ["lazy", "sleep", "weight", "slow"]

        vata = sum([2 for word in vata_keywords if word in symptom])
        pitta = sum([2 for word in pitta_keywords if word in symptom])
        kapha = sum([2 for word in kapha_keywords if word in symptom])

        total = vata + pitta + kapha + 1

        vata_score = vata/total*100
        pitta_score = pitta/total*100
        kapha_score = kapha/total*100

        st.subheader("📊 Dosha Analysis")

        # Chart
        labels = ['Vata', 'Pitta', 'Kapha']
        values = [vata_score, pitta_score, kapha_score]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        st.pyplot(fig)

        # Result
        if vata_score > pitta_score and vata_score > kapha_score:
            dominant = "Vata"
            reason = "Stress, dryness, or irregular lifestyle detected"
            diet = "Warm, cooked foods"
            lifestyle = "Meditation, regular routine"
            herbs = "Ashwagandha"

        elif pitta_score > kapha_score:
            dominant = "Pitta"
            reason = "Heat, acidity, or anger detected"
            diet = "Cooling foods, avoid spicy"
            lifestyle = "Relaxation, avoid heat"
            herbs = "Amla, Coconut water"

        else:
            dominant = "Kapha"
            reason = "Laziness, heaviness detected"
            diet = "Light, spicy foods"
            lifestyle = "Exercise, active routine"
            herbs = "Ginger, Honey"

        st.success(f"Dominant Dosha: {dominant}")

        st.write("🧠 **Reason:**", reason)

        st.subheader("🌿 Recommendations")

        st.write("🍽️ Diet:", diet)
        st.write("🧘 Lifestyle:", lifestyle)
        st.write("🌿 Herbs:", herbs)

# ---------------- LEARN ----------------
elif menu == "Learn Ayurveda":
    st.header("📚 Ayurveda Learning")

    topic = st.selectbox("Select Topic", ["Vata", "Pitta", "Kapha"])

    if topic == "Vata":
        st.write("Controls movement. Imbalance causes anxiety and dryness.")

    elif topic == "Pitta":
        st.write("Controls digestion. Imbalance causes heat and anger.")

    elif topic == "Kapha":
        st.write("Provides stability. Imbalance causes laziness.")