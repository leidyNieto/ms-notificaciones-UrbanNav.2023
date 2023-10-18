from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
from decouple import config

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>¡Está funcionando bien! :D</p>"

@app.route("/sms", methods=['POST'])
def send_sms_sns():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        numero_telefono = data.get('numero_telefono', '')

        if mensaje and numero_telefono:
            client = boto3.client(
                "sns",
                aws_access_key_id=config("AWS_API_KEY"),
                aws_secret_access_key=config("AWS_SECRET_KEY"),
                region_name="us-east-2"
            )
            client.publish(
                PhoneNumber=numero_telefono,
                Message=mensaje
            )
            return "<p>SMS enviado!</p>"
        else:
            return "<p>Parámetros faltantes en la solicitud.</p>", 400
    except Exception as e:
        print(f'Error: {str(e)}')
        return "<p>Error en el servidor.</p>", 500

@app.route("/email", methods=['POST'])
def send_email_ses():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        correo_destinatario = data.get('correoDestino', '')

        if mensaje and correo_destinatario:
            SENDER = "Andres Rios <andresrios774@gmail.com>"
            AWS_REGION = "us-east-2"
            SUBJECT = "Código de verificación"
            BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "Este correo electrónico fue enviado con Amazon SES utilizando el "
                "AWS SDK para Python (Boto).")
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>Amazon SES Test (SDK para Python)</h1>
                <p>Este correo electrónico fue enviado con
                    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> utilizando el
                    <a href='https://aws.amazon.com/sdk-for-python/'>
                    AWS SDK para Python (Boto)</a>.</p>
                <p>{mensaje}</p>
                </body>
                </html>"""
            
            CHARSET = "UTF-8"

            client = boto3.client(
                "ses",
                aws_access_key_id=config("AWS_API_KEY"),
                aws_secret_access_key=config("AWS_SECRET_KEY"),
                region_name="us-east-2"
            )
            response = client.send_email(
                Destination={'ToAddresses': [correo_destinatario]},
                Message={
                    'Body': {
                        'Html': {'Charset': CHARSET, 'Data': BODY_HTML},
                        'Text': {'Charset': CHARSET, 'Data': BODY_TEXT},
                    },
                    'Subject': {'Charset': CHARSET, 'Data': SUBJECT},
                },
                Source=SENDER,
            )
            return f"<p>Correo electrónico enviado a {correo_destinatario}! ID del mensaje: {response['MessageId']}</p>"
        else:
            return "<p>Parámetros faltantes en la solicitud.</p>", 400
    except Exception as e:
        print(f'Error: {str(e)}')
        return "<p>Error en el servidor.</p>", 500

if __name__ == "__main__":
    app.run()