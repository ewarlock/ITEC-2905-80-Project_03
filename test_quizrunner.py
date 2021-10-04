import unittest
from unittest import TestCase

import quizrunner

from quizdatabase import Question


class TestQuiz(TestCase):


    def test_trim_list(self):
        initial_list = [1, 2, 3, 4, 5]
        max_length_list = 3

        expected_list = [1, 2, 3]

        new_list = quizrunner.trim_list(initial_list, max_length_list)

        self.assertEqual(expected_list, new_list)


    def test_trim_list_past_list_length(self):
        initial_list = [1, 2, 3, 4, 5]
        max_length_list = 10

        expected_list = [1, 2, 3, 4, 5]

        returned_list = quizrunner.trim_list(initial_list, max_length_list)

        self.assertEqual(expected_list, returned_list)
    

    def test_create_answer_list(self):
        question = Question(question='Test Question One', answercorrect='Correct Answer', answerincorrecta='Incorrect A', answerincorrectb='Incorrect B', answerincorrectc='Incorrect C', difficulty=1, points=1, category='Category')

        expected_list = ['Correct Answer', 'Incorrect A', 'Incorrect B', 'Incorrect C']

        returned_list = quizrunner.create_answer_list(question)

        self.assertEqual(expected_list, returned_list)


    def test_grade_question_when_correct(self):
        correct_answer = 'Correct Answer'
        user_answer = 'Correct Answer'

        expected = 1

        returned = quizrunner.grade_question(correct_answer, user_answer)

        self.assertEqual(expected, returned)


    def test_grade_question_when_not_correct(self):
        correct_answer = 'Correct Answer'
        user_answer = 'Incorrect B'

        expected = 0

        returned = quizrunner.grade_question(correct_answer, user_answer)

        self.assertEqual(expected, returned)


    def test_grade_question_when_not_correct_and_emojis(self):
        correct_answer = 'Correct Answer'
        user_answer = '👻👻👻👻👻'

        expected = 0

        returned = quizrunner.grade_question(correct_answer, user_answer)

        self.assertEqual(expected, returned)


    def test_grade_question_when_not_correct_and_empty_string(self):
        correct_answer = 'Correct Answer'
        user_answer = ''

        expected = 0

        returned = quizrunner.grade_question(correct_answer, user_answer)

        self.assertEqual(expected, returned)


    def test_grade_question_when_not_correct_and_integer(self):
        correct_answer = 'Correct Answer'
        user_answer = 100

        expected = 0

        returned = quizrunner.grade_question(correct_answer, user_answer)

        self.assertEqual(expected, returned)



if __name__ == '__main__':
    unittest.main()