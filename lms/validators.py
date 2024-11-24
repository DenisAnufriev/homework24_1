from rest_framework.exceptions import ValidationError

allowed_names = ["youtube.com", "youtu.be"]


def validate_youtube_only(value):
    if value.lower().split("//")[1] not in allowed_names:
        raise ValidationError("Ссылка на видео должна быть только с YouTube")
