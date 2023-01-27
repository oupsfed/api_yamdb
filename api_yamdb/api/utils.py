from django.core.mail import send_mail


def send_token(code, username, email):
    return send_mail(
        subject='Ваш код аутентификации',
        message='Сохраните код! Он понадобится вам для получения токена.\n'
                f'confirmation_code:\n{code}\n'
                f'username: {username}',
        from_email='admn@yamdb.com',
        recipient_list=[email],
        fail_silently=False,
    )
