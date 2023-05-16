from src.tasks.celery_config import celery_app
from PIL import Image
from pathlib import Path

@celery_app.task # celery принимает только базовые форматы, модель алхимии он не примет для типизации // исправить убрать коммент
def process_pic( # Это не io задача, поэтому, можно синхронную функцию // исправить, с асинхронностью спорный момент
        path: str
):
    im_path = Path(path)  # Логически разделяет путь и можем обратиться к файлу
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))  # Указываем размер
    im_resized_200_100 = im.resize((200, 100))  # Маленькое изображение, для иконок

    im_resized_1000_500.save(f'src/cars/images/resized_1000_500{im_path.name}')  # задаём путь и имя

    im_resized_200_100.save(f'src/cars/images/resized_200_100{im_path.name}')  # задаём путь и имя

    # Далее прописывааем задачу в роутере на загрузку картинок

# @celery.task # пока закоментил, т.к. не прописал данные по гугл почте
# def send_bookin_confirmation_email(
#         booking: dict,
#         email_to: EmailStr
# ):
#     # email_to_mock = settings.SMTP_USER # Для теста отправляем сами себе
#     msg_content = create_booking_confirmation_template(booking, email_to)
#     with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
#         server.login(settings.SMTP_USER, settings.SMTP_PASS)
#         server.send_message(msg_content) # отправляем письмо