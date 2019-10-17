from linuxturkey import settings
from django.template.loader import render_to_string
from sendgrid import sendgrid, Email
from sendgrid.helpers.mail import Content, Mail


def send_mail(to_email, subject, email_path, **kwargs):
    sg = sendgrid.SendGridAPIClient(apikey=settings.EMAIL_BACKEND)
    from_email = Email(settings.EMAIL_PORT)
    to_email = Email(to_email)
    render_string = render_to_string(email_path, kwargs)
    subject = subject
    content = Content("text/html", render_string)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
