from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название курса"
    )
    preview = models.ImageField(
        upload_to="lms/course/preview/",
        verbose_name="Превью",
        help_text="Загрузите превью курса",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание курса"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название урока"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="lms/lesson/preview/",
        verbose_name="Превью",
        help_text="Загрузите превью урока",
        **NULLABLE
    )
    link_to_video = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, **NULLABLE, related_name="lesson"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
