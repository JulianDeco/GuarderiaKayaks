from smtplib import SMTP_SSL as SMTP  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SMTP_HOST = "smtp.resend.com"
SMTP_PORT = 465 
SMTP_USERNAME = "resend"
SMTP_PASSWORD = os.getenv("RESEND_API_KEY")

def aviso_mail_plantilla(nombre_cliente, fecha_vencimiento):
    html_aviso = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vencimiento de Pago</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    background-color: #ffffff;
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }}
                .header h1 {{
                    margin: 0;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    line-height: 1.6;
                }}
                .content .highlight {{
                    font-weight: bold;
                    color: #d9534f;
                }}
                .cta {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .cta a {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 4px;
                    font-size: 16px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #888888;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Recordatorio de Vencimiento de Pago</h1>
                </div>
                <div class="content">
                    <p>Estimado/a <b>{nombre_cliente}</b>,</p>
                    <p>Este es un recordatorio de que su factura tiene un pago pendiente con fecha de vencimiento el <span class="highlight">{fecha_vencimiento}</span>.</p>
                    <p>Le solicitamos por favor que realice el pago lo antes posible para evitar cualquier inconveniente.</p>
                    <p>Si ya ha realizado el pago, por favor ignore este mensaje.</p>
                    <p>Gracias por su atención.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Su Empresa. Todos los derechos reservados.</p>
                    <p><a href="#">Contactar Soporte</a></p>
                </div>
            </div>
        </body>
        </html>
    """
    return html_aviso

def envio_mail(destinatarios, asunto, nombre_cliente, fecha_vencimiento, enviado_de="El refugio del remo <onboarding@resend.dev>"):
    try:
        cuerpo_html = aviso_mail_plantilla(nombre_cliente, fecha_vencimiento)

        mensaje = MIMEMultipart()
        mensaje["From"] = enviado_de
        mensaje["To"] = ", ".join(destinatarios)
        mensaje["Subject"] = asunto

        mensaje.attach(MIMEText(cuerpo_html, "html"))
        conn = SMTP(SMTP_HOST)
        conn.set_debuglevel(False)
        conn.login(SMTP_USERNAME, SMTP_PASSWORD)

        conn.sendmail(enviado_de, destinatarios, mensaje.as_string())
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error enviando correo: {e}")
        