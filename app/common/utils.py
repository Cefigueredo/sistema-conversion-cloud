import requests
from os import getenv

EMAIL_DOMAIN = getenv("EMAIL_DOMAIN")
EMAIL_API_KEY = getenv("EMAIL_API_KEY")


def send_message(file_name, old_format, new_format, email):
    r = requests.post(
        f"https://api.mailgun.net/v3/{EMAIL_DOMAIN}/messages",
        auth=("api", EMAIL_API_KEY),
        data={
            "from": f"Excited User <mailgun@{EMAIL_DOMAIN}>",
            "to": [email],
            "subject": "Tarea de conversión completada, ya puedes descargar tu archivo",
            "text": f"La conversión de el archivo {file_name}.{old_format} a {new_format} fue exitosa. Puedes descargarlo con el nombre {file_name}.{new_format}",
        },
    )
    print(r.text)


if __name__ == "__main__":
    send_message("test", "mp3", "ogg", "sergiodavidchecho@outlook.com")
