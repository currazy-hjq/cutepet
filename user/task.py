from django.core.mail import send_mail
from cutepet.celery import app


@app.task
def send_active_email(email, url):
    subject = '萌宠乐用户激活邮件'
    html_message = '''
        <p>尊敬的用户您好<p>
        <p>激活操作请<a href='%s' target='blank'>点击激活</a></p>
        ''' % url
    send_mail(subject, '', '1006923031@qq.com', html_message=html_message, recipient_list=[email])
