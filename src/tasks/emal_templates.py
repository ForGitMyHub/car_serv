from email.message import EmailMessage # стандартная библиотека

from pydantic import EmailStr


# При большом объеме задач это может забивать оперативную память.
# В нагруженных приложениях рекомендуется отдавать только идентификатор объекта в базе данных.
# Celery во время выполнения задачи сам обратится к базе данных, достанет данные о брони и затем отправит письмо
def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr # только для проверки корректности почты, в celery не отдаём, он этот тип не понимает
):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования' # Тема письма
    # email['From'] = settings.SMTP_USER # .env // почта с которой делаем рассылку
    email['To'] = email_to # имейл пользователя

    email.set_content(
        f'''
            <h1> </h1> 
            Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        ''',
        subtype='html' # Чтобы была конвертация в html
    )
    return email