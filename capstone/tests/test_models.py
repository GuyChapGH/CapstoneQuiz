from django.test import TestCase
from django.utils.timezone import localtime

from capstone.models import User, Question, Quiz, Contest

# Create your tests here.

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()
        
        # Create question
        Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')

    def test_answer0_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer0').max_length
        self.assertEqual(max_length, 30)

    def test_answer1_max_length(self):
            question = Question.objects.get(id=1)
            max_length = question._meta.get_field('answer1').max_length
            self.assertEqual(max_length, 30)

    def test_answer2_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer2').max_length
        self.assertEqual(max_length, 30)

    def test_answer3_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('answer3').max_length
        self.assertEqual(max_length, 30)

    def test_correct_answer_max_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('correct_answer').max_length
        self.assertEqual(max_length, 30)
    
    def test_object_name_is_question_content(self):
        question = Question.objects.get(id=1)
        expected_object_name = f'Question: {question.content}'
        self.assertEqual(str(question), expected_object_name)

class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create user
        test_user1 = User.objects.create_user(username = 'testuser1', password='testpassword')
        test_user1.save()
        
        # Create question
        test_question = Question.objects.create(user=test_user1, content='Is this a test question?', answer0='Yes', answer1='No', answer2='No', answer3='No', correct_answer='answer0')
        test_question.save()

        # Create quiz
        test_quiz = Quiz.objects.create(user=test_user1, quiz_name='test_quiz1')
        test_quiz.questions.add(test_question)
        test_quiz.save()


    def test_quiz_name_max_length(self):
        quiz = Quiz.objects.get(id=1)
        max_length = quiz._meta.get_field('quiz_name').max_length
        self.assertEqual(max_length, 30)

    def test_quiz_name_is_quiz_name(self):
        quiz = Quiz.objects.get(id=1)
        expected_object_name = f'{quiz.quiz_name}'
        self.assertEqual(str(quiz), expected_object_name)

class ContestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create user
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

    def test_contest_name_is_user_name_timestamp_quiz_name(self):
        contest = Contest.objects.get(id=1)
        local_timestamp = localtime(contest.timestamp)
        local_timestamp_form = local_timestamp.strftime("%a, %d %b %Y %H:%M:%S")
        expected_object_name = f"{contest.user.username} at {local_timestamp_form}. Quizname: {contest.quiz.quiz_name}."
        self.assertEqual(str(contest), expected_object_name)

    def test_contest_quiz_question_is_test_question_content(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_question = "Is this a test question?"
        self.assertEqual(contest.question(n), expected_question)

    def test_contest_quiz_question_is_index_error_with_n_out_of_range(self):
        contest = Contest.objects.get(id=1)
        n = 1
        with self.assertRaises(IndexError):
            contest.question(n)

    def test_multiple_choice0_is_answer0(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_answer = "Yes"
        self.assertEqual(contest.multiple_choice0(n), expected_answer)

    def test_multiple_choice1_is_answer1(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_answer = "No"
        self.assertEqual(contest.multiple_choice1(n), expected_answer)

    def test_multiple_choice2_is_answer2(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_answer = "No"
        self.assertEqual(contest.multiple_choice2(n), expected_answer)

    def test_multiple_choice3_is_answer3(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_answer = "No"
        self.assertEqual(contest.multiple_choice3(n), expected_answer)

    def test_correct_answer_is_answer0(self):
        contest = Contest.objects.get(id=1)
        n = 0
        expected_answer = "answer0"
        self.assertEqual(contest.correct_answer(n), expected_answer)

    def test_questions_in_quiz_is_1(self):
        contest = Contest.objects.get(id=1)
        expected_question_count = "1"
        self.assertEqual(contest.questions_in_quiz(), expected_question_count)

    def test_q_score_default_is_0(self):
        contest = Contest.objects.get(id=1)
        expected_default_score = "0"
        self.assertEqual(contest.q_score(), expected_default_score)

    def test_q_score_increases_by_1_with_score_point(self):
        """This test modifies the test data. Might need to set up special data for this case"""
        contest = Contest.objects.get(id=1)
        contest.score_point()
        expected_score = "1"
        self.assertEqual(contest.q_score(), expected_score)