from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class CreateQuestionViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Create question
        Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

    def test_redirect_if_not_logged_in(self):
        # Get response
        response = self.client.get(reverse("create_question"))
        self.assertRedirects(response, "/login?next=/create_question/")

    def test_logged_in_user_uses_correct_template(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("create_question"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/create_question.html")

    def test_logged_in_user_contains_question_last_in_context(self):       
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("create_question"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that context contains question_last
        self.assertContains(response, "Is this a test question?")

        # Check that context does not contain 'No Saved Questions.'
        self.assertNotContains(response, "No Saved Questions.")

    def test_logged_in_user_has_no_question_last(self):
        # Delete all questions
        Question.objects.all().delete()
        
        # Login and get repsonse
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("create_question"))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that context contains 'No Saved Questions.'
        self.assertContains(response, "No Saved Questions.")


