from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import random
import smtplib
import ssl
import string
from IdeaBox.settings import STATICFILES_DIRS, config_mail


def generate_random_token(length):
    characters = list(string.ascii_letters + string.digits)
    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    token = []
    for i in range(length):
        token.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(token)

    # converting the list to string
    # printing the list
    return "".join(token)


def send_mail(sujet, html, attachments, image_path, destinataire, cc, emetteur=config_mail['sender']):
    message = MIMEMultipart()
    message['From'] = emetteur
    message['To'] = destinataire
    message['Cc'] = cc
    message['Subject'] = sujet
    # bcc = 'cyril.henry@gmail.com, ' + config_mail['sender']
    bcc = ''
    to_addresse = destinataire + ',' + cc + ',' + bcc

    full_html = """\
    <html>
        <head></head>
        <body>
            <img src="cid:image1" alt="Logo" style="width:50px; height:50px;"><br>
            """ + html + """
        </body>
    </html>
    """
    part2 = MIMEText(full_html, 'html')
    message.attach(part2)

    path = os.path.join(STATICFILES_DIRS[0], 'img/logo_mail.png')
    fp = open(path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    if image_path != "":
        fp = open(image_path, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(image_path))
        message.attach(img)

    for filename in attachments:
        with open(filename, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}",)
            message.attach(part)
    ssl_context = ssl.create_default_context()

    server = smtplib.SMTP_SSL(config_mail['smtp_server'], config_mail['smtp_port'])
    server.ehlo()
    server.starttls
    server.login(config_mail['login'], config_mail['password'])
    server.sendmail(emetteur, to_addresse, message.as_string())
    print("Mail envoyé à ", to_addresse)
    server.quit()