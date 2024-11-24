from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from lms.paginations import CustomPagination
from lms.models import Course, Lesson
from users.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsModerator | IsOwner]
        else:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class LessonListCreateAPIView(ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [~IsModerator, IsOwner]
        else:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "DELETE":
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()
