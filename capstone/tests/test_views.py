from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class CreateQuestionViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("create_question"))
        self.assertRedirects(response, "/capstone/login/")

    def test_logged_in_user_uses_correct_template(self):
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("create_question"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/create_question.html")