from rest_framework.exceptions import ValidationError


def validate_youtube_only(value):
    allowed_names = ["youtube.com", "youtu.be"]
    if not any(name in value.lower() for name in allowed_names):
        raise ValidationError(
            "Ссылка должна быть только на ресурсы YouTube (youtube.com или youtu.be)"
        )
