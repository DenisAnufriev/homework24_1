from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_course_update(course_id, course_title, user_emails):
    course = f"Обновление курса: {course_title}"
    message = f"Курс '{course_title}' был обновлён. Проверьте материалы!"
    from_email = settings.EMAIL_HOST_USER
    for email in user_emails:
        send_mail(course, message, from_email, [email])
    print("Уведомление об обновлении курса разосланы")
