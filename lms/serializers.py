from rest_framework import serializers
from rest_framework.fields import IntegerField, BooleanField
from drf_spectacular.utils import extend_schema_field

from lms.models import Course, Lesson
from lms.validators import validate_youtube_only
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    link_to_video = serializers.URLField(validators=[validate_youtube_only])

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "link_to_video",
            "course",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )

    @extend_schema_field(IntegerField)
    def get_lessons_count(self, obj):
        return obj.lessons.count()

    @extend_schema_field(BooleanField)
    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()
