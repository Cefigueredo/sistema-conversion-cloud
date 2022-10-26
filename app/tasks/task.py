import os
from common.utils import send_message
from models import ConversionTask, User
from celery import Celery
from models import TaskStatus

# from pydub import AudioSegment

FILES_FOLDER = os.getenv("FILES_FOLDER")


celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BROKER_URL"),
)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery.conf.beat_schedule = {
    "add-every-20-seconds": {
        "task": "conversion_task",
        "schedule": 20.0,
    },
}

celery.conf.timezone = "UTC"

"""
@celery.task(name="conversion_task", bind=True)
def conversion_task():

    tasks = ConversionTask.query.with_for_update().filter(
        ConversionTask.status == "UPLOADED"
    )
    for task in tasks:
        if task:
            print(f"Convirtiendo archivo {task.file_name} a {task.new_file_format}")
        try:
            old_file_format = task.file_name.split(".")[-1]
            if task.new_file_format == "mp3":
                AudioSegment.from_file(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{old_file_format}",
                    old_file_format,
                ).export(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{task.new_file_format}",
                    format="mp3",
                )
            elif task.new_file_format == "wma":
                AudioSegment.from_file(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{old_file_format}",
                    old_file_format,
                ).export(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{task.new_file_format}",
                    format="wma",
                )
            elif task.new_file_format == "ogg":
                AudioSegment.from_file(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{old_file_format}",
                    old_file_format,
                ).export(
                    f"{FILES_FOLDER}/{task.user}/{task.file_name}.{task.new_file_format}",
                    format="ogg",
                )
            else:
                print("Formato no soportado")
            task.status = TaskStatus.PROCESSED.value
            task.update()
            user = User.query().filter(User.id == task.user).first()
            if user:
                send_message(
                    task.file_name,
                    old_file_format,
                    task.new_file_format,
                    user.email,
                )
            else:
                print("No se pudo enviar el correo")

        except Exception as e:
            task.rollback()
            return f"Error procesando Conversión: {e}", 409
        else:
            print("Exitoso!!!!!!!")
"""


@celery.task(name="conversion_task", bind=True)
def conversion_task(*args):
    tasks = ConversionTask.query.with_for_update().filter(
        ConversionTask.status == "UPLOADED"
    )
    for task in tasks:
        if task:
            print(f"Convirtiendo archivo {task.file_name} a {task.new_file_format}")
        try:
            old_file_format = task.file_name.split(".")[-1]
            name_task = task.file_name.split(".")[0]
            os.rename(
                f"{FILES_FOLDER}/{task.user}/{task.file_name}",
                f"{FILES_FOLDER}/{task.user}/{name_task}.{task.new_format}",
            )
            task.file_name = name_task + "." + task.new_format
            task.status = TaskStatus.PROCESSED.value
            task.update()
            user = User.query().filter(User.id == task.user).first()
            if user:
                send_message(
                    task.file_name,
                    old_file_format,
                    task.new_file_format,
                    user.email,
                )
            else:
                print("No se pudo enviar el correo")

        except Exception as e:
            task.rollback()
            return f"Error procesando Conversión: {e}", 409
        else:
            print("Exitoso!!!!!!!")
