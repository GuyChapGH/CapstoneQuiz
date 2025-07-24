from django.test import TestCase
from django.urls import reverse

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class PlayQuizViewTest(TestCase):
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

        # Create contest
        test_contest = Contest.objects.create(user=test_user1, quiz=test_quiz)
        test_contest.save()

    def test_redirect_if_not_logged_in(self):
        # Get response
        contest_id = Contest.objects.all().last().id
        response = self.client.get(reverse("play_quiz", args=(contest_id,)))

        self.assertRedirects(response, "/login?next=/play_quiz/1")

    def test_logged_in_user_uses_correct_template(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        
        contest_id = Contest.objects.all().last().id
        response = self.client.get(reverse("play_quiz", args=(contest_id,)))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), "testuser1")

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200) 

        # Check that we used correct template
        self.assertTemplateUsed(response, "capstone/play_quiz.html")

class PlayQuizViewDatabaseTest(TestCase):
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

        # Create contest
        test_contest = Contest.objects.create(user=test_user1, quiz=test_quiz)
        test_contest.save()

    def test_context_contains_all_data_when_logged_in(self):
        # Login and get response
        login = self.client.login(username = 'testuser1', password='testpassword')
        
        
        contest_id = Contest.objects.all().last().id
        response = self.client.get(reverse("play_quiz", args=(contest_id,)))

        # Check context includes all contest data

        self.assertTrue(response.context['question'], "Is this a test question?")
        
        self.assertTrue(response.context['multiple_choice0'], 'Yes') 
        self.assertTrue(response.context['multiple_choice1'], 'No') 
        self.assertTrue(response.context['multiple_choice2'], 'No') 
        self.assertTrue(response.context['multiple_choice3'], 'No') 

        self.assertTrue(response.context['correct_answer'], 'answer0')

        self.assertTrue(response.context['number_questions'], 1)         