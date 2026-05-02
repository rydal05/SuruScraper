# temporary notification implentation for use when running suruscraper locally.
from plyer import notification

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )