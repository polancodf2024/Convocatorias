import streamlit as st
from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
from datetime import datetime
import pytz

# Configuración
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "abcdf2024dfabc@gmail.com"
EMAIL_PASSWORD = "hjdd gqaw vvpj hbsy"
NOTIFICATION_EMAIL = "polanco@unam.mx"
CSV_CONVOCATORIAS_FILE = "registro_convocatorias.csv"

# Selección de idioma
idioma = st.sidebar.selectbox("Idioma", ["Español", "English"], index=0)

# Función para registrar datos en CSV (registro_convocatorias.csv)
def registrar_convocatoria(nombre, numero_economico):
    tz_mexico = pytz.timezone("America/Mexico_City")
    fecha_actual = datetime.now(tz_mexico)
    fecha_hora = fecha_actual.strftime("%Y,%m,%d,%H,%M")
    estado = "Activo"
    fecha_terminacion = ""

    encabezados = ["Fecha y Hora", "Nombre Completo", "Número Económico", "Estado", "Fecha de Terminación"]
    datos = [fecha_hora, nombre, numero_economico, estado, fecha_terminacion]

    try:
        with open(CSV_CONVOCATORIAS_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Escribe encabezados si el archivo está vacío
                writer.writerow(encabezados)
            writer.writerow(datos)
    except Exception as e:
        st.error(f"Error al registrar convocatoria: {e}")

# Función para enviar notificación al administrador con el archivo CSV
def enviar_notificacion_administrador():
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = NOTIFICATION_EMAIL
        mensaje['Subject'] = "Nuevo registro en convocatorias"

        cuerpo = (
            f"Se ha recibido un nuevo registro en el sistema. Consulta el archivo adjunto." 
            if idioma == "Español" else 
            "A new registration has been added to the system. Check the attached file."
        )
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Adjuntar el archivo CSV
        with open(CSV_CONVOCATORIAS_FILE, "rb") as attachment:
            part_csv = MIMEBase("application", "octet-stream")
            part_csv.set_payload(attachment.read())
        encoders.encode_base64(part_csv)
        part_csv.add_header("Content-Disposition", f"attachment; filename={CSV_CONVOCATORIAS_FILE}")
        mensaje.attach(part_csv)

        # Enviar correo
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, NOTIFICATION_EMAIL, mensaje.as_string())
    except Exception as e:
        st.error(f"Error al enviar notificación al administrador: {e}")

# Función para enviar confirmación al usuario
def enviar_confirmacion_usuario(email, nombre):
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_USER
        mensaje['To'] = email
        mensaje['Subject'] = "Confirmación de registro" if idioma == "Español" else "Registration Confirmation"

        cuerpo = (
            f"Hola {nombre}, hemos recibido tu registro exitosamente. Gracias por participar."
            if idioma == "Español" else 
            f"Hello {nombre}, your registration has been successfully received. Thank you for participating."
        )
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Enviar correo
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, email, mensaje.as_string())
    except Exception as e:
        st.error(f"Error al enviar confirmación al usuario: {e}")

# Añadir logo y título
st.image("escudo_COLOR.jpg", width=100)
st.title("Registro Para Recibir Convocatorias" if idioma == "Español" else "Registro Para Recibir Convocatorias")

# Solicitar información del usuario
nombre_completo = st.text_input("Nombre completo" if idioma == "Español" else "Full Name")
numero_economico = st.text_input("Número Económico" if idioma == "Español" else "Economic Number")
email = st.text_input("Correo electrónico" if idioma == "Español" else "Email Address")
email_confirmacion = st.text_input("Confirma tu correo electrónico" if idioma == "Español" else "Confirm Your Email")

# Procesar envío
if st.button("Enviar" if idioma == "Español" else "Submit"):
    if not nombre_completo or not numero_economico or not email or not email_confirmacion:
        st.error("Por favor, completa todos los campos correctamente." if idioma == "Español" else "Please complete all fields correctly.")
    elif email != email_confirmacion:
        st.error("Los correos electrónicos no coinciden." if idioma == "Español" else "Email addresses do not match.")
    else:
        with st.spinner("Registrando..." if idioma == "Español" else "Registering..."):
            # Registrar en el archivo CSV
            registrar_convocatoria(nombre_completo, numero_economico)

            # Enviar confirmación al usuario
            enviar_confirmacion_usuario(email, nombre_completo)

            # Notificar al administrador con el archivo CSV
            enviar_notificacion_administrador()

            st.success("Registro completado exitosamente." if idioma == "Español" else "Registration completed successfully.")

