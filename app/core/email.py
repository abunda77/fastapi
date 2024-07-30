from smtplib import SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from app.core.config import settings  # Import settings from config.py

def send_welcome_email(email: str, subject="Selamat bergabung di BOSQUE PROPERTI!"):
    """
    Sends a welcome email to a new user.

    Args:
        email (str): The email address of the new user.
        subject (str, optional): The subject of the email. Defaults to "Welcome to BOSQUE PROPERTI!".
    """

    try:
        # Use settings from config.py for email configuration
        #mail_mailer = settings.MAIL_MAILER
        mail_host = settings.MAIL_HOST
        
        mail_port = settings.MAIL_PORT
        mail_username = settings.MAIL_USERNAME
        mail_password = settings.MAIL_PASSWORD
        mail_encryption = settings.MAIL_ENCRYPTION
        mail_from_address = settings.MAIL_FROM_ADDRESS

        message = MIMEMultipart("alternative")
        message["From"] = formataddr((settings.PROJECT_NAME, mail_from_address))
        message["To"] = email
        message["Subject"] = subject

        # Create plain text and HTML versions of the email content (modify as needed)
        text_part = MIMEText("Welcome to BOSQUE PROPERTI! Thank you for signing up.", "plain")
        html_part = MIMEText('''\
        <html>
        <body>
            <h1>Welcome to BOSQUE PROPERTI!</h1>
            <p>Thank you for signing up. We're excited to have you on board.</p>
        </body>
        </html>
        ''', "html")
        message.attach(text_part)
        message.attach(html_part)

        # Create a secure connection with the SMTP server
        with SMTP(mail_host, mail_port) as server:
            if mail_encryption:
                server.noop()
            server.login(mail_username, mail_password)
            server.sendmail(mail_from_address, [email], message.as_string())

        print(f"Welcome email successfully sent to {email}")
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")

# Example usage (assuming email is a user.User object)
# send_welcome_email(email.email)
