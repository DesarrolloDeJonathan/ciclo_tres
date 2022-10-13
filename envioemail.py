import smtplib # Libreria para configurar el sistema de envio
from email.message import EmailMessage # Instanciar clase de una libreria para estructurar el envio del mensaje

def enviar(email_destino,asunto,mensaje):
    try:
        email_origen="jonathan.cardozo.dev@outlook.com" # usuario uninorte o correo outlook
        password="udnwmEqsn*XSmu!" #aqui password de su outlook
        email = EmailMessage()
        email["From"] = email_origen
        email["To"] = email_destino
        email["Subject"] = asunto
        email.set_content(mensaje)

    # Send Email
        # Cada servidor o gestor de correo requiere su servidor para el protoco lo SMTP
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587) # instancia de variable en ese puerto
        smtp.starttls()
        smtp.login(email_origen, password)
        smtp.sendmail(email_origen, email_destino, email.as_string())
        smtp.quit()
        return "1"
    except :
        return "0"
