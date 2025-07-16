from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.


class QuizSelectViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        # Get response
        response = self.client.get(reverse("quiz_select"))
        self.assertRedirects(response, "/login?next=/quiz_select/")

    def test_logged_in_user_uses_correct_template(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("quiz_select"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/quiz_select.html") 

class QuizSelectViewDatabaseTest(TestCase):
    def test_create_contest_and_redirect_to_play_quiz_when_submitting_valid_form(self):
        """Test that form submission with valid data creates a contest in the database"""
  
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Login user
        login = self.client.login(username = 'testuser1', password='testpassword')

        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

        test_question.save()

        # Create quiz
        test_quiz = Quiz.objects.create(user=test_user1, quiz_name='test_quiz1')
        test_quiz.questions.add(test_question)
        test_quiz.save()
        
        form_data = {
            'quiz': test_quiz           
        }

        response = self.client.post(reverse('quiz_select'), data=form_data)

        # Check that the contest was created and we were redirected
        self.assertEqual(response.status_code, 302) # Redirect after form submission
        
        # Contest should be in the database
        self.assertTrue(Contest.objects.exists())        

        # NB: THIS TEST DOESNT WORK. form_data doesnt select test_quiz and Contest object is not created.

    def test_doesnt_create_contest_and_returns_to_form_when_submitting_invalid_form(self):
        """Test that form submission with invalid data does not create a contest in the database"""
  
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

        # Login user
        login = self.client.login(username = 'testuser1', password='testpassword')

        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

        test_question.save()

        # Create quiz
        test_quiz = Quiz.objects.create(user=test_user1, quiz_name='test_quiz1')
        test_quiz.questions.add(test_question)
        test_quiz.save()
        
        # Form data
        form_data = {
            'quiz': '' # Quiz needs to be selected so should fail           
        }

        response = self.client.post(reverse('quiz_select'), data=form_data)

        # Check that we get a 200 status (stay on the page to correct errors)
        self.assertEqual(response.status_code, 200)

        # Check error messages in form response
        self.assertTrue("form" in response.context)

        form = response.context['form']

        self.assertFormError(form, 'quiz', 'This field is required.')

        self.assertFalse(Contest.objects.exists()) # No Contest should be in the database 
