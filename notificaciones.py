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

@app.route("/pqrs", methods=['POST'])
def send_pqrs_email():
    try:
        data = request.get_json()
        print(f'Solicitud recibida: {data}')  # Imprimir la solicitud recibida
        tipo = data.get('tipo', '')
        mensaje = data.get('mensaje', '')
        correo_destinatario = "andresrios774@gmail.com" 

        if tipo and mensaje:
            SENDER = "Andres <andresrios774@gmail.com>" 
            AWS_REGION = "us-east-2"
            SUBJECT = f"PQRS - {tipo}"
            BODY_TEXT = f"Tipo de PQRS: {tipo}\n\n{mensaje}"
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>PQRS - {tipo}</h1>
                <p>{mensaje}</p>
                </body>
                </html>"""

            CHARSET = "UTF-8"

            client = boto3.client(
                "ses",
                aws_access_key_id=config("AWS_API_KEY"),
                aws_secret_access_key=config("AWS_SECRET_KEY"),
                region_name=AWS_REGION
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
    
@app.route("/factura", methods=['POST'])
def send_factura_email():
    try:
        data = request.get_json()
        print(f'Solicitud recibida: {data}')  # Imprimir la solicitud recibida
        nombre = data.get('nombre', '')
        fecha = data.get('fecha', '')
        costo = data.get('costo', '')
        correo = data.get('correo', '') 

        if fecha and costo and nombre and correo:
            SENDER = "Andres <andresrios774@gmail.com>" 
            AWS_REGION = "us-east-2"
            SUBJECT = f"Factura electronica - {nombre} - {fecha}"
            BODY_TEXT = f"Factura de viaje de {nombre}"
            BODY_HTML = f"""<html>
                <head>
                    <style>
                        h1 {{
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Factura de Viaje</h1>
                    <p>Nombre: {nombre}</p>
                    <p>Fecha: {fecha}</p>
                    <p>Costo: {costo}</p>
                    <p>Correo: {correo}</p>
                </body>
            </html>"""

            CHARSET = "UTF-8"

            client = boto3.client(
                "ses",
                aws_access_key_id=config("AWS_API_KEY"),
                aws_secret_access_key=config("AWS_SECRET_KEY"),
                region_name=AWS_REGION
            )
            response = client.send_email(
                Destination={'ToAddresses': [correo]},
                Message={
                    'Body': {
                        'Html': {'Charset': CHARSET, 'Data': BODY_HTML},
                        'Text': {'Charset': CHARSET, 'Data': BODY_TEXT},
                    },
                    'Subject': {'Charset': CHARSET, 'Data': SUBJECT},
                },
                Source=SENDER,
            )
            return f"<p>Correo electrónico enviado a {correo}! ID del mensaje: {response['MessageId']}</p>"
        else:
            return "<p>Parámetros faltantes en la solicitud.</p>", 400
    except Exception as e:
        print(f'Error: {str(e)}')
        return "<p>Error en el servidor.</p>", 500
    

@app.route("/panico", methods=['POST'])
def send_boton_panico():
    try:
        data = request.get_json()
        print(f'Solicitud recibida: {data}')  # Imprimir la solicitud recibida
        ruta = data.get('ruta', '')
        datos_conductor = data.get('datos_conductor', '')
        datos_usuario = data.get('datos_usuario', '')
        numero_telefono = data.get('numero_telefono', '')  # Agregué este campo para el número de teléfono de ayuda

        if datos_conductor and datos_usuario and ruta and numero_telefono:
            AWS_REGION = "us-east-2"
            SUBJECT = "Alguien presionó el botón de pánico"
            MESSAGE = f"El usuario {datos_usuario} está teniendo problemas en la ruta {ruta} que está a cargo del conductor {datos_conductor}"

            client = boto3.client(
                "sns",
                aws_access_key_id=config("AWS_API_KEY"),
                aws_secret_access_key=config("AWS_SECRET_KEY"),
                region_name=AWS_REGION
            )

            response = client.publish(
                PhoneNumber=numero_telefono,
                Message=MESSAGE,
                Subject=SUBJECT
            )

            return f"<p>Mensaje de texto enviado a {numero_telefono}! ID del mensaje: {response['MessageId']}</p>"
        else:
            return "<p>Parámetros faltantes en la solicitud.</p>", 400
    except Exception as e:
        print(f'Error: {str(e)}')
        return "<p>Error en el servidor.</p>", 500
    
if __name__ == "__main__":
    app.run()