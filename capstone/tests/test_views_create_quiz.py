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
            'questions': 1
        }

        response = self.client.post(reverse('create_quiz'), data=form_data)

        # Check that the quiz was created and we were redirected
        self.assertEqual(response.status_code, 302) # Redirects after successful form submission
        self.assertTrue(Quiz.objects.filter(quiz_name='test_quiz1').exists()) # Quiz should be in the database

    def test_dont_create_quiz_when_submitting_invalid_form(self):
        """Test that form submission with invalid data fails to create a quiz in the database"""
  
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
            'quiz_name': '', # quiz_name required so should fail 
            'questions': 1
        }

        response = self.client.post(reverse('create_quiz'), data=form_data)


        # Check that the quiz failed to create and we stay on page with error message
        self.assertEqual(response.status_code, 200) # Stays on page after failed form submission showing errors

        # Check error messages in form response
        self.assertTrue("form" in response.context)

        form = response.context['form']

        # Test for error message
        self.assertEqual(form.errors['quiz_name'][0], 'This field is required.')

        # Test no quiz in database
        self.assertFalse(Quiz.objects.exists()) # There should be no quiz in the database

    def test_dont_create_quiz_when_submitting_duplicate_quiz_name_invalid_form(self):
        """Test that form submission with duplicate quiz_name invalid data fails to create a quiz in the database"""
  
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


        # Set up data for POST to view
        form_data = {
            'user': test_user1,
            'quiz_name': 'test_quiz1', # quiz_name duplicated so should fail 
            'questions': 1
        }

        response = self.client.post(reverse('create_quiz'), data=form_data)


        # Check that the quiz failed to create and we stay on page with error message
        self.assertEqual(response.status_code, 200) # Stays on page after failed form submission showing errors

        # Check error messages in form response
        self.assertTrue("form" in response.context)

        form = response.context['form']

        # Test for error message
        self.assertEqual(form.errors['quiz_name'][0], 'Quiz with this Quiz name already exists.')

        # Test only one quiz in database
        self.assertEqual(Quiz.objects.count(), 1) # There should only be one quiz in the database (created in set up)
