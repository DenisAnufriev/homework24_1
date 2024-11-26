from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from lms.models import Course, Lesson
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    - Аутентифицированные пользователи видят свои курсы.
    - Модераторы видят все курсы.
    - Разграничение прав доступа: владельцы или модераторы в зависимости от действия.
    """

    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает queryset курсов в зависимости от прав пользователя.
        - Анонимные пользователи получают пустой queryset.
        - Модераторы видят все курсы.
        - Обычные пользователи видят только свои курсы.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Сохраняет курс с текущим пользователем как владельцем.
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Устанавливает права доступа в зависимости от действия:
        - create: доступ запрещён модераторам.
        - destroy: доступ разрешён только владельцу.
        - update/partial_update/retrieve: доступ разрешён владельцу и модератору.
        """
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
    """
    APIView для создания и получения списка уроков.

    - Аутентифицированные пользователи видят свои уроки.
    - Модераторы видят все уроки.
    - Разграничение прав доступа: владельцы или модераторы в зависимости от действия.
    """
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от прав пользователя.
        - Анонимные пользователи получают пустой queryset.
        - Модераторы видят все уроки.
        - Обычные пользователи видят только свои уроки.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """
        Устанавливает права доступа в зависимости от метода:
        - POST: доступ разрешён владельцам, запрещён модераторам.
        - GET: доступ разрешён владельцам и модераторам.
        """
        if self.request.method == "POST":
            self.permission_classes = [~IsModerator, IsOwner]
        else:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Сохраняет урок с текущим пользователем как владельцем.
        """
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    APIView для чтения, обновления и удаления конкретного урока.

    - Аутентифицированные пользователи видят свои уроки.
    - Модераторы видят все уроки.
    - Разграничение прав доступа: владельцы или модераторы в зависимости от действия.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от прав пользователя.
        - Анонимные пользователи получают пустой queryset.
        - Модераторы видят все уроки.
        - Обычные пользователи видят только свои уроки.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        """
        Устанавливает права доступа в зависимости от метода:
        - DELETE: доступ разрешён только владельцу.
        - GET/PUT/PATCH: доступ разрешён владельцам и модераторам.
        """
        if self.request.method == "DELETE":
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()
