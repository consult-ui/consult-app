from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


async def send_email(
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        subject: str,
        message_body: str
) -> None:
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587

    msg: MIMEMultipart = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    async with aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port) as server:
        await server.login(sender_email, sender_password)
        await server.sendmail(sender_email, recipient_email, msg.as_string())
