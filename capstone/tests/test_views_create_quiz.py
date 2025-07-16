from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class CreateQuizViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

        test_question.save()

        # Create quiz
        test_quiz = Quiz.objects.create(user=test_user1, quiz_name='test_quiz1')
        test_quiz.questions.add(test_question)
        test_quiz.save()

    def test_redirect_if_not_logged_in(self):
        # Get response
        response = self.client.get(reverse("create_quiz"))
        self.assertRedirects(response, "/login?next=/create_quiz/")

    def test_logged_in_user_uses_correct_template(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("create_quiz"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/create_quiz.html")

    # Add tests for list of questions in form checkbox
    # More tests.
    #       Test_questions_form_field_shows_check_box_select_multiple_widget

class CreateQuizViewDatabaseTest(TestCase):
    def test_create_quiz_when_submitting_valid_form(self):
        """Test that form submission with valid data creates a quiz in the database"""
  
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Login user
        login = self.client.login(username = 'testuser1', password='testpassword')

        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

        test_question.save()

        form_data = {
            'user': test_user1,
            'quiz_name': 'test_quiz1', 
            #'questions': test_question
        }

        response = self.client.post(reverse('create_quiz'), data=form_data)

        # NB: THIS TEST DOESNT WORK. 
        #  Don't know how to create test Quiz object. 
        # form_data approach does not work because questions is a many-to-many field
        # many-to-many field requires instance to be created in database first
        # Don't know how to reference this object in database so can 'add' questions.
        # ????.questions.add(test_question)
        # ????.save()

        # Check that the quiz was created and we were redirected
        self.assertEqual(response.status_code, 302) # Redirect after form submission
        self.assertTrue(Quiz.objects.filter(quiz_name='test_quiz1').exists()) # Quiz should be in the database
