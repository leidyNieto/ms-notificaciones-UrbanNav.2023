from flask import Flask
import boto3
from botocore.exceptions import ClientError
from decouple import config

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Esta funcionando bien :D</p>"

@app.route("/sms")
def send_sms_sns():
    # Crear un cliente de SNS
    client = boto3.client(
        "sns",
        aws_access_key_id=config("AWS_API_KEY"),
        aws_secret_access_key=config("AWS_SECRET_KEY"),
        region_name="us-east-2"
    )
    # Enviar tu mensaje de SMS.
    client.publish(
        PhoneNumber="+573225872380",
        Message="Hola Andres desde SNS!"
    )
    return "<p>SMS enviado!</p>"

@app.route("/email")
def send_email_ses():
    # El remitente del correo electrónico.
    SENDER = "Andres Rios <andresrios774@gmail.com>"

    # El destinatario del correo electrónico.
    RECIPIENT = "andresrios774@gmail.com"

    # El conjunto de configuración de Amazon SES.
    CONFIGURATION_SET = "PruebasNFProg3"

    #Región de AWS
    AWS_REGION = "us-east-2"

    SUBJECT = "Hola desde SES"

    # El cuerpo del correo electrónico para los clientes que no admiten HTML.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "Este correo electrónico fue enviado con Amazon SES utilizando el "
                "AWS SDK para Python (Boto)."
                )
                
    # El cuerpo HTML del correo electrónico.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK para Python)</h1>
    <p>Este correo electrónico fue enviado con
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> utilizando el
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK para Python (Boto)</a>.</p>
    </body>
    </html>
                """            

    CHARSET = "UTF-8"

    client = boto3.client(
                    "ses",
                    aws_access_key_id=config("AWS_API_KEY"),
                    aws_secret_access_key=config("AWS_SECRET_KEY"),
                    region_name="us-east-2"
                )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("¡Correo electrónico enviado! ID del mensaje:"),
        print(response['MessageId'])
    return "<p>Correo electrónico enviado! ID del mensaje: " + response['MessageId'] + "</p>"

if __name__ == "__main__":
    app.run()