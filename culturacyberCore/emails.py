from django.core.mail import send_mail
from django.contrib.auth.models import User
import os

def verification_email(account):

    mail_template_file = os.path.join(os.path.dirname(__file__), 'templates/mails/activate_account.html')
    mail_template = ''.join(open(mail_template_file, 'r', encoding="UTF-8").readlines())

    user = User.objects.get(username=account)

    new_mail = mail_template.replace('{{usermail}}', str(user.email))
    new_mail = new_mail.replace('{{useruuid}}', str(user.extend.uuid))
    
    send_mail(
        'Correo de confirmación plataforma CulturaCyber',
        'Cultura Cybertrust',
        'culturacyber@cybertrust.cl',
        [user.email],
        fail_silently=False,
        html_message=new_mail
    )