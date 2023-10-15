from celery import shared_task

from mail.services.mail_manager import MailSenderManager


@shared_task
def send_mail_in_background(**kwargs):
    status = MailSenderManager().send(**kwargs)
    return status
