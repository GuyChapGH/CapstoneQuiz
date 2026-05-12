from django.test import TestCase

from capstone.forms import QuestionCreateForm, QuizCreateForm, ContestSelectForm, ResultsSelectForm

# Create your tests here.

class TestQuestionCreateForm(TestCase):
    def test_empty_form(self):
        form = QuestionCreateForm()
        self.assertIn("content", form.fields)
        self.assertIn("answer0", form.fields)
        self.assertIn("answer1", form.fields)
        self.assertIn("answer2", form.fields)
        self.assertIn("answer3", form.fields)
        self.assertIn("correct_answer", form.fields)

    def test_content_field_label(self):
        form = QuestionCreateForm()
        self.assertTrue(form.fields['content'].label is None or form.fields['content'].label == 'Question')

    def test_answer0_field_label(self):
        form = QuestionCreateForm()
        self.assertTrue(form.fields['answer0'].label is None or form.fields['answer0'].label == 'Answer A')

    def test_answer1_field_label(self):
        form = QuestionCreateForm()
        self.assertTrue(form.fields['answer1'].label is None or form.fields['answer1'].label == 'Answer B')

    def test_answer2_field_label(self):
        form = QuestionCreateForm()
        self.assertTrue(form.fields['answer2'].label is None or form.fields['answer2'].label == 'Answer C')

    def test_answer3_field_label(self):
        form = QuestionCreateForm()
        self.assertTrue(form.fields['answer3'].label is None or form.fields['answer3'].label == 'Answer D')

    # More tests.
    #       Test_correct_answer_form_field_shows_radio_select_widget

class TestQuizCreateForm(TestCase):
    def test_empty_form(self):
        form = QuizCreateForm()
        self.assertIn("quiz_name", form.fields)
        self.assertIn("questions", form.fields)

    # More tests.
    #       Test_questions_form_field_shows_check_box_select_multiple_widget

class TestContestSelectForm(TestCase):
    def test_empty_form(self):
        form = ContestSelectForm()
        self.assertIn("quiz", form.fields)

class TestResultsSelectForm(TestCase):
    def test_empty_form(self):
        form = ResultsSelectForm()
        self.assertIn("quiz", form.fields)
