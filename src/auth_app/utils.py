from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import logging 

logger = logging.getLogger(__name__)

def send_mail_with_body_html(subject: str, recipient_list: list, template: str, context: dict ):
    
    message = render_to_string(template_name=template, context=context)
    
    try:
        send_mail(subject=subject,
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  fail_silently=True,
                  html_message=message,
                  recipient_list=recipient_list
                  )
        return True
    
    except Exception as e:
        logger.error(e)
    return False