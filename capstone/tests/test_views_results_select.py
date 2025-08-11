from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class ResultsSelectViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        # Get response
        response = self.client.get(reverse("results_select"))
        self.assertRedirects(response, "/login?next=/results_select/")

    def test_logged_in_user_uses_correct_template(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        response = self.client.get(reverse("results_select"))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/results_select.html") 

class ResultsSelectViewDatabaseTest(TestCase):
    def test_select_quiz_and_redirect_to_results_display_when_submitting_valid_form(self):
        """Test that form submission with valid data redirects to results display"""
  
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
        
        # Get POST response
        form_data = {
            'quiz': 1 # This should select the quiz with quiz_id=1           
        }

        response = self.client.post(reverse('results_select'), data=form_data)

        # Check that the quiz was selected (how to do this?) and we were redirected
        self.assertEqual(response.status_code, 302) # Redirect after form submission 

    def test_stay_on_current_page_with_form_errors_when_submitting_invalid_form(self):
        """Test that form submission with invalid data stays on current page and shows error message"""
  
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
        
        # Get POST response
        form_data = {
            'quiz': '' # quiz is required so this should fail          
        }

        response = self.client.post(reverse('results_select'), data=form_data)

        # Check that this gives form error and we stay on same page
        self.assertEqual(response.status_code, 200) # stay on form page to correct error  

        # Check error messages in form response
        self.assertTrue("form" in response.context)

        form = response.context['form']

        # Test for error message
        self.assertEqual(form.errors['quiz'][0], 'This field is required.')
        
   