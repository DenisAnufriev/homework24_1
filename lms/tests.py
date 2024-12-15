from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, Lesson
from users.models import Subscription, User


class CourseAndLessonTests(APITestCase):
    def setUp(self):
        self.moderator_group = Group.objects.create(name="moderator")

        self.owner_user = User.objects.create(
            email="test@test.com", password="12345678"
        )
        self.moderator_user = User.objects.create(
            email="moderator@test.com", password="12345678"
        )
        self.moderator_user.groups.add(self.moderator_group)

        self.client = APIClient()

        self.course = Course.objects.create(
            title="Test Course", description="Course description", owner=self.owner_user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson description",
            link_to_video="http://youtube.com",
            course=self.course,
            owner=self.owner_user,
        )

    def test_create_course_as_owner(self):
        """
        Проверяет, что владелец может создать новый курс.
        """
        self.client.force_authenticate(user=self.owner_user)
        data = {"title": "test", "description": "test"}
        response = self.client.post("/learning/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_create_course_as_moderator(self):
        """
        Проверяет, что модератор не может создать новый курс.
        """
        self.client.force_authenticate(user=self.moderator_user)
        data = {"title": "test", "description": "test"}
        response = self.client.post("/learning/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_course_as_owner(self):
        """
        Проверяет, что владелец может получить информацию о курсе.
        """
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(f"/learning/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)

    def test_retrieve_course_as_moderator(self):
        """
        Проверяет, что модератор может получить информацию о курсе.
        """
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(f"/learning/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)

    def test_update_course_as_owner(self):
        """
        Проверяет, что владелец может обновить информацию о курсе.
        """
        self.client.force_authenticate(user=self.owner_user)
        data = {"title": "Updated Course", "description": "Updated description"}
        response = self.client.patch(f"/learning/courses/{self.course.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course")

    def test_update_course_as_moderator(self):
        """
        Проверяет, что модератор может обновить информацию о курсе.
        """
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            "title": "Updated Course by Moderator",
            "description": "Updated description by moderator",
        }
        response = self.client.patch(f"/learning/courses/{self.course.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course by Moderator")

    def test_delete_course_as_owner(self):
        """
        Проверяет, что владелец может удалить курс.
        """
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(f"/learning/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_delete_course_as_moderator(self):
        """
        Проверяет, что модератор может удалить курс.
        """
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(f"/learning/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_and_unsubscribe(self):
        """
        Проверяет, что пользователь может подписаться и отписаться от курса.
        """
        self.client.force_authenticate(user=self.owner_user)

        data = {"course_id": self.course.id}
        response = self.client.post("/users/subs/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")

        subscription = Subscription.objects.filter(
            user=self.owner_user, course=self.course
        )
        self.assertTrue(subscription.exists())

        response = self.client.post("/users/subs/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")

        subscription = Subscription.objects.filter(
            user=self.owner_user, course=self.course
        )
        self.assertFalse(subscription.exists())


class LessonTest(APITestCase):
    def setUp(self):
        self.moderator_group = Group.objects.create(name="moderator")

        self.owner_user = User.objects.create(
            email="test@test.com", password="12345678"
        )
        self.moderator_user = User.objects.create(
            email="moderator@test.com", password="12345678"
        )
        self.moderator_user.groups.add(self.moderator_group)

        self.client = APIClient()

        self.course = Course.objects.create(
            title="Test Course", description="Course description", owner=self.owner_user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson description",
            link_to_video="http://youtube.com",
            course=self.course,
            owner=self.owner_user,
        )

    def test_create_lesson_as_owner(self):
        """
        Проверяет, что владелец может создать новый урок.
        """
        self.client.force_authenticate(user=self.owner_user)
        data = {
            "title": "test",
            "description": "test",
            "link_to_video": "http://youtube.com",
            "course": self.course.id,
        }
        response = self.client.post("/learning/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_as_moderator(self):
        """
        Проверяет, что модератор не может создать новый урок.
        """
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            "title": "test",
            "description": "test",
            "link_to_video": "http://youtube.com",
            "course": self.course.id,
        }
        response = self.client.post("/learning/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson_as_owner(self):
        """
        Проверяет, что владелец может получить информацию об уроке.
        """
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(f"/learning/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_retrieve_lesson_as_moderator(self):
        """
        Проверяет, что модератор может получить информацию об уроке.
        """
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(f"/learning/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_update_lesson_as_owner(self):
        """
        Проверяет, что владелец может обновить информацию об уроке.
        """
        self.client.force_authenticate(user=self.owner_user)
        data = {"title": "Updated Lesson", "description": "Updated description"}
        response = self.client.patch(f"/learning/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_moderator(self):
        """
        Проверяет, что модератор может обновить информацию об уроке.
        """
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            "title": "Updated Lesson by Moderator",
            "description": "Updated description by moderator",
        }
        response = self.client.patch(f"/learning/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson by Moderator")

    def test_delete_lesson_as_owner(self):
        """
        Проверяет, что владелец может удалить урок.
        """
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(f"/learning/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_as_moderator(self):
        """
        Проверяет, что модератор может удалить урок.
        """
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(f"/learning/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
