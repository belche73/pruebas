import streamlit as st

# Título de la aplicación
st.title('Mi primera aplicación con Streamlit')

# Crear un cuadro de texto
nombre = st.text_input('¿Cuál es tu nombre?')

# Crear un control deslizante
edad = st.slider('¿Cuál es tu edad?', 0, 100, 25)

# Mostrar la información
if nombre:
    st.write(f'Hola, {nombre}. Tienes {edad} años.')

# Botón para mostrar un mensaje
if st.button('Saludar'):
    st.success(f'¡Saludos, {nombre}!')

# Mostrar gráficos simples
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Gráfico de Seno')

st.pyplot(fig)