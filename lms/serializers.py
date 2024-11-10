from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "link_to_video", "course",)


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson")

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lessons_count", "lessons",)

    def get_lessons_count(self, obj):
        return obj.lesson.count()
