import streamlit as st
from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime
import pytz

# Configuración de idioma con español como predeterminado
idioma = st.sidebar.selectbox("Idioma", ["Español", "English"], index=0)

# Configuración de correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"
NOTIFICATION_EMAIL = "polanco@unam.mx"
CSV_FILE = "interesados.convocatorias.csv"
MAX_FILE_SIZE_MB = 20

# Función para guardar la información en el archivo CSV
def save_to_csv(nombre, email):
    data = {"Nombre": [nombre], "Email": [email]}
    df = pd.DataFrame(data)
    if not Path(CSV_FILE).exists():
        df.to_csv(CSV_FILE, index=False)
    else:
        existing_df = pd.read_csv(CSV_FILE)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(CSV_FILE, index=False)

# Función para enviar correo de confirmación
def send_confirmation(email_usuario, nombre_usuario, idioma):
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_USER
    mensaje['To'] = email_usuario
    mensaje['Subject'] = "Confirmación de registro" if idioma == "Español" else "Registration Confirmation"
    
    cuerpo = (f"Hola {nombre_usuario},\n\nGracias por registrarte en nuestras convocatorias. Te contactaremos pronto.\n\n"
              "Atentamente,\nCentro de Registro a Convocatorias" if idioma == "Español"
              else f"Hello {nombre_usuario},\n\nThank you for registering for our research proposals. We will contact you soon.\n\n"
                   "Best regards,\nCalls Team")
    
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, email_usuario, mensaje.as_string())

# Añadir el logo y el título de la página
st.image("escudo_COLOR.jpg", width=100)
st.title("Centro de Registro a Convocatorias" if idioma == "Español" else "Call for Research Proposals")

# Solicitar nombre y correo electrónico
nombre_usuario = st.text_input("Nombre completo" if idioma == "Español" else "Full Name")
email_usuario = st.text_input("Correo electrónico" if idioma == "Español" else "Email Address")
email_confirmacion = st.text_input("Confirma tu correo electrónico" if idioma == "Español" else "Confirm Your Email")

# Botón para enviar la información
if st.button("Enviar" if idioma == "Español" else "Submit"):
    if not nombre_usuario:
        st.error("Por favor, ingresa tu nombre completo." if idioma == "Español" else "Please enter your full name.")
    elif not email_usuario or not email_confirmacion:
        st.error("Por favor, ingresa y confirma tu correo electrónico." if idioma == "Español" else "Please enter and confirm your email.")
    elif email_usuario != email_confirmacion:
        st.error("Los correos electrónicos no coinciden." if idioma == "Español" else "The email addresses do not match.")
    else:
        # Guardar la información en el archivo CSV
        save_to_csv(nombre_usuario, email_usuario)

        # Enviar correo de confirmación
        send_confirmation(email_usuario, nombre_usuario, idioma)

        st.success("Registro completado y correo de confirmación enviado." if idioma == "Español" else "Registration completed and confirmation email sent.")


