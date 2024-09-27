import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from algorithms.mailing_service.main import get_all_emails


def send_aqi_alert_to_subscribers(recipient_list: list, aqi_message: str):
    # Email server settings for Gmail
    HOST = "smtp.gmail.com"
    PORT = 587
    FROM_EMAIL = "codesteinsprojectmail@gmail.com"  # Replace with your Gmail address
    APP_PASSWORD = "omgk mmrb ywjn dwes"  # Replace with your app password

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['Subject'] = "Important: Air Quality Index Alert"

    # HTML formatted email body
    body_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                color: #555;
            }}
            .header {{
                background-color: #343a40;
                color: #fff;
                padding: 10px;
                text-align: center;
            }}
            .content {{
                margin: 20px;
                font-size: 16px;
            }}
            .alert {{
                color: #d9534f;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #aaa;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Air Quality Index Alert</h2>
        </div>
        <div class="content">
            <p>Dear Subscriber,</p>
            <p>This is an important notification regarding the current air quality in your area.</p>
            <p class="alert">The current Air Quality Index (AQI) level is: <strong>{aqi_message}</strong></p>
            <p>We recommend taking precautions and limiting outdoor activities until conditions improve.</p>
            <p>Stay safe and healthy!</p>
        </div>
        <div class="footer">
            <p>Thank you for being a part of our community.</p>
            <p>Webai AQI Team</p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(body_content, 'html'))

    try:
        # Establish connection to the SMTP server
        with smtplib.SMTP(HOST, PORT) as server:
            server.starttls()  # Secure the connection
            server.login(FROM_EMAIL, APP_PASSWORD)  # Log in with your Gmail credentials

            # Send the email to all recipients using BCC
            msg['Bcc'] = ', '.join(recipient_list)  # Set the "Bcc" field correctly
            server.sendmail(FROM_EMAIL, recipient_list, msg.as_string())

            print(f"Email sent successfully to {len(recipient_list)} recipients via BCC!")

    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")


def send_email_notification(aqi_message: str = "This is a trial message. Please Ignore. Inconvenience is regretted."):
    emails = get_all_emails()

    send_aqi_alert_to_subscribers(emails, aqi_message)


# send_email_notification()

