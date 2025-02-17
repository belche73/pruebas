import streamlit as st
import os
import google.generativeai as genai

# Configura la página de Streamlit
st.set_page_config(
    page_title="Planificador de Viajes",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título y formulario de entrada
st.title("✈️ Planificador de Viajes")
st.write("Ingresa tus preferencias y obten un plan de viaje personalizado.")

with st.form(key="travel_form"):
    destino = st.text_input("¿A dónde quieres viajar?")
    mes = st.text_input("¿Qué mes quieres viajar?")
    dias = st.number_input("¿Cuántos días quieres viajar?", min_value=1, step=1)
    submit_button = st.form_submit_button(label="Planificar viaje")

# Genera el plan de viaje con Gemini
if submit_button:
    os.environ["API_KEY"] = "AIzaSyCBuIg1-6kl5D4xELrSYwY5dQhuh3M9noo"  # Reemplaza con tu API KEY
    genai.configure(api_key=os.environ["API_KEY"])

    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash",
      generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    pregunta = f"Prepara un plan de viaje a {destino} durante {mes} para {dias} días."

    response = chat_session.send_message(pregunta)
    st.markdown(response.text) # Muestra el plan en formato markdown
