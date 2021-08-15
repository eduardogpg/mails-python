import ssl
import smtplib

from pathlib import Path

from jinja2 import Environment 
from jinja2 import FileSystemLoader

from email import encoders

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from decouple import config

def render_template(template, context):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template(template)
    return template.render(**context)


def attach_file(message, file):
    path = Path(file)
    attachment = open(path, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    part.add_header(
        'Content-Disposition',
        'attachment',
        filename=path.name
    )

    encoders.encode_base64(part)
    message.attach(part)
    

def send_mail(receiver_mail, subject, template, context, cc=None, files=[]):
    sender = 'eduardo78d@gmail.com'

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver_mail

    if cc:
        message['Cc'] = cc

    content = render_template(template, context)

    content = MIMEText(content, 'html')
    message.attach(content)

    if files:
        for file in files:
            attach_file(message, file)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
        server.login(sender, config('EMAIL_PASSWORD'))

        server.send_message(message)

        print('Mensaje enviado exitosamente!')

if __name__ == '__main__':

    send_mail(
        'eduardogpg2@gmail.com',
        'Un correo mejor estructurado',
        'welcome.html',
        {
            'username': 'Eduardo GPG',
            'series': ['Expresiones regulares', 'Envío de correos']
        },
        'eduardo78d@gmail.com',
        [
            'README.md', 'main.py'
        ]
    )