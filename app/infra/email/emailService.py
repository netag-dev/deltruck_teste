# emailService.py

import logging

from app.utils.singletonMeta import SingletonMeta

from flask_mail import Message
from flask import current_app
from app.extensions import mail


class EmailService(metaclass=SingletonMeta):

    def send_email(self, subject, recipients, body):
        try:
            msg = Message(
                subject,
                sender=current_app.config["MAIL_DEFAULT_SENDER"],
                recipients=[recipients],
            )
            msg.body = body
            mail.send(msg)
            logging.info("EmailService.send_email(): Email enviado com sucesso!")
        except Exception as e:
            logging.error("Erro ao enviar email: %s", {str(e)})
