import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from src.config import settings

logger = logging.getLogger() # Получаем логгер

logHandler = logging.StreamHandler() # Устанавливаем хэндлер (То, куда будет писаться лог, в данном случае, в консоль)




class CustomJsonFormatter(jsonlogger.JsonFormatter): # Formater - форматирует лог
    # Код взят из документации
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

# formatter = jsonlogger.JsonFormatter()#
logHandler.setFormatter(formatter) # Прикрепляем форматер к хэндлеру
logger.addHandler(logHandler) # Добавляем хэндлер
logger.setLevel(settings.LOG_LEVEL) # Задали уровень логгирования