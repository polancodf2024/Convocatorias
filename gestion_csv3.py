import streamlit as st
import os
from pathlib import Path
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Configuración del archivo CSV y correo
CSV_FILE = "interesados.convocatorias.csv"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"

# Solicitar contraseña al inicio
PASSWORD = "Tt5plco5"
input_password = st.text_input("Ingresa la contraseña para acceder:", type="password")

# Verificar la contraseña
if input_password != PASSWORD:
    st.error("Contraseña incorrecta. No tienes acceso a esta página.")
    st.stop()

# Título de la aplicación
st.title("Gestión de Archivo: interesados.convocatorias.csv")

# Opción para subir el archivo interesados.convocatorias.csv
st.header("Subir el archivo interesados.convocatorias.csv")
uploaded_csv = st.file_uploader("Selecciona el archivo para subir y reemplazar el existente", type=["csv"])

if uploaded_csv is not None:
    try:
        # Guardar el archivo subido temporalmente
        temp_file = "temp_interesados.csv"
        with open(temp_file, "wb") as f:
            f.write(uploaded_csv.getbuffer())

        # Reemplazar el archivo existente usando el comando de Linux cp
        os.system(f"cp {temp_file} {CSV_FILE}")
        st.success("Archivo interesados.convocatorias.csv subido y reemplazado exitosamente.")

        # Mostrar una vista previa del archivo subido
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)

        # Eliminar el archivo temporal
        os.remove(temp_file)

    except Exception as e:
        st.error("Error al subir el archivo. Por favor, intenta nuevamente.")
        st.error(str(e))

# Opción para descargar el archivo interesados.convocatorias.csv
st.header("Descargar el archivo interesados.convocatorias.csv")

if Path(CSV_FILE).exists():
    try:
        with open(CSV_FILE, "rb") as file:
            st.download_button(
                label="Descargar interesados.convocatorias.csv",
                data=file,
                file_name="interesados.convocatorias.csv",
                mime="text/csv"
            )
        st.success("Archivo listo para descargar.")
    except Exception as e:
        st.error("Error al descargar el archivo.")
        st.error(str(e))
else:
    st.warning("El archivo interesados.convocatorias.csv no existe.")

# Opción para subir un archivo PDF
st.header("Subir un archivo PDF para enviar como adjunto")
uploaded_pdf = st.file_uploader("Selecciona un archivo PDF para enviar a todos los correos registrados", type=["pdf"])

# Función para enviar el PDF como adjunto
def enviar_pdf_adjuntos(pdf_path):
    try:
        # Leer la lista de correos electrónicos del archivo CSV
        df = pd.read_csv(CSV_FILE)
        correos = df["Email"].tolist()

        # Configurar la conexión SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)

            # Enviar el correo a cada destinatario individualmente
            for correo in correos:
                # Crear un nuevo mensaje para cada destinatario
                mensaje = MIMEMultipart()
                mensaje['From'] = EMAIL_USER
                mensaje['To'] = correo
                mensaje['Subject'] = "Envío de Convocatoria Adjunta"
                cuerpo = "Estimado usuario,\n\nAdjunto encontrarás el PDF de la convocatoria.\n\nSaludos cordiales."

                mensaje.attach(MIMEText(cuerpo, 'plain'))

                # Adjuntar el archivo PDF
                with open(pdf_path, "rb") as pdf_file:
                    adjunto = MIMEApplication(pdf_file.read(), _subtype="pdf")
                    adjunto.add_header('Content-Disposition', 'attachment', filename="convocatoria.pdf")
                    mensaje.attach(adjunto)

                # Enviar el correo
                server.sendmail(EMAIL_USER, correo, mensaje.as_string())

        st.success("Archivo PDF enviado exitosamente a todos los correos registrados.")

    except Exception as e:
        st.error("Error al enviar el archivo PDF.")
        st.error(str(e))

# Botón para enviar el PDF como adjunto
if uploaded_pdf is not None:
    try:
        # Guardar el archivo PDF temporalmente
        temp_pdf = "temp_convocatoria.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        # Botón para enviar el archivo PDF
        if st.button("Enviar PDF a todos los correos"):
            enviar_pdf_adjuntos(temp_pdf)
            # Eliminar el archivo temporal después de enviarlo
            os.remove(temp_pdf)

    except Exception as e:
        st.error("Error al procesar el archivo PDF.")
        st.error(str(e))

