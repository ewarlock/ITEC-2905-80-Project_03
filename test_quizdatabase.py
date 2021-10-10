
import unittest 
from unittest import TestCase
from unittest.mock import patch
from peewee import *

import db_config
test_db_path = 'test_quiz.db'
db_config.database_path = test_db_path 

import quizdatabase
from quizdatabase import Question
from quizdatabase import Result
from quizdatabase import QuizDBError

class TestQuiz(TestCase):

    test_db_url = 'test_quiz.db'

    """
    Before running these test, test_quiz.db
    Create expected Question table & Result table
    """

    def setUp(self):
        '''Clear and remake Question and Result tables for test database.'''
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Question, Result])
        self.db.create_tables([Question, Result])


    def test_get_all_questions_with_questions_in_db(self):
        # TODO: make this become an error or error message instead of an empty list?
        sample_question_one = Question(question='Test Question One', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category')
        sample_question_two = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category')
        sample_question_one.save()
        sample_question_two.save()

        empty_list = []

        questions = quizdatabase.get_all_questions()

        self.assertNotEqual(questions, empty_list)


    def test_get_all_categories(self):
        sample_question_one = Question(question='Test Question One', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category One')
        sample_question_two = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category One')
        sample_question_three = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category Two')
        sample_question_one.save()
        sample_question_two.save()
        sample_question_three.save()

        expected = ['Category Two', 'Category One']

        categories = quizdatabase.get_category_list()

        self.assertCountEqual(categories, expected)


    def test_get_all_questions_no_questions_in_db_raises_QuizDBError(self):
        with self.assertRaises(QuizDBError):
            questions = quizdatabase.get_all_questions()

    
    def test_get_questions_by_category_valid_category(self):
        sample_question_one = Question(question='Test Question One', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category One')
        sample_question_two = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category One')
        sample_question_three = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category Two')
        sample_question_one.save()
        sample_question_two.save()
        sample_question_three.save()

        category = 'Category One'
        empty_list = []

        questions = quizdatabase.get_questions_by_category(category)

        self.assertNotEqual(questions, empty_list)


    def test_get_questions_by_category_invalid_category_raises_QuizDBError(self):
        category = 'Category One'

        with self.assertRaises(QuizDBError):
            questions = quizdatabase.get_questions_by_category(category)


    def test_get_question_by_id_valid_id(self):
        sample_question_one = Question(question='Test Question One', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category')
        sample_question_two = Question(question='Test Question Two', answercorrect='Yes', answerincorrecta='No', answerincorrectb='No', answerincorrectc='No', difficulty=1, points=1, category='Category')
        sample_question_one.save()
        sample_question_two.save()

        questions = quizdatabase.get_question_by_id(2)

        self.assertIsNotNone(questions)


    def test_get_question_by_id_not_in_database_raises_QuizDBError(self):
        with self.assertRaises(QuizDBError):
            questions = quizdatabase.get_question_by_id(2)


    def test_get_question_by_weird_character_id_not_in_database_raises_QuizDBError(self):
        with self.assertRaises(QuizDBError):
            questions = quizdatabase.get_question_by_id('👻👻👻👻👻')


    def test_convert_boolean_to_number_for_is_correct_when_False(self):
        is_correct = False

        is_correct_number = quizdatabase.convert_is_correct_to_number(is_correct)
        expected = 0

        self.assertEqual(is_correct_number, expected)


    def test_convert_boolean_to_number_for_is_correct_when_True(self):
        is_correct = True

        is_correct_number = quizdatabase.convert_is_correct_to_number(is_correct)
        expected = 1

        self.assertEqual(is_correct_number, expected)


    def test_convert_boolean_to_number_for_is_correct_when_invalid_raises_QuizDBError(self):
        is_correct = '👻👻👻👻👻/\/lskdjf\'    '

        with self.assertRaises(QuizDBError):
            is_correct_number = quizdatabase.convert_is_correct_to_number(is_correct)


    def test_convert_boolean_to_number_for_is_correct_accepts_0_as_False(self):
        is_correct = 0

        is_correct_number = quizdatabase.convert_is_correct_to_number(is_correct)
        expected = 0

        self.assertEqual(is_correct_number, expected)        


    def test_convert_boolean_to_number_for_is_correct_accepts_1_as_True(self):
        is_correct = 1

        is_correct_number = quizdatabase.convert_is_correct_to_number(is_correct)
        expected = 1

        self.assertEqual(is_correct_number, expected)


    def test_create_question_result_valid_result(self):
        timestamp_start = 1234
        timestamp_end = 5678
        user_answer = 'This is an answer'
        points = 3
        is_correct = True
        session_id = 12345
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, session_id, question_id)

        result = Result.get_or_none()
        self.assertIsNotNone(result)
        

    def test_create_question_result_with_weird_result(self):
        timestamp_start = 1234
        timestamp_end = 5678
        user_answer = '👻👻👻👻👻/\/lskdjf\'    '
        points = 3
        is_correct = True
        session_id = 12345
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, session_id, question_id)

        result = Result.get_or_none()
        self.assertIsNotNone(result)


    def test_get_last_session_id(self):
        timestamp_start = 1
        user_answer = 'This is an answer'
        points = 3
        is_correct = 1
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, 10, user_answer, points, is_correct, 'Session One', question_id)

        expected = 'Session One'

        last_session_id = quizdatabase.get_last_session_id()

        self.assertEqual(last_session_id, expected)


    def test_get_last_session_id_when_no_results_in_db_raises_QuizDBError(self):
        with self.assertRaises(QuizDBError):
            last_session_id = quizdatabase.get_last_session_id()


    def test_get_last_session_results(self):
        timestamp_start = 1
        user_answer = 'This is an answer'
        points = 3
        is_correct = 1
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, 10, user_answer, points, is_correct, 'Session One', question_id)
        quizdatabase.create_question_result(timestamp_start, 20, user_answer, points, is_correct, 'Session Two', question_id)
        quizdatabase.create_question_result(timestamp_start, 30, user_answer, points, is_correct, 'Session Two', question_id)
        quizdatabase.create_question_result(timestamp_start, 40, user_answer, points, is_correct, 'Session Three', question_id)
        quizdatabase.create_question_result(timestamp_start, 50, user_answer, points, is_correct, 'Session Three', question_id)

        expected = 'Session Three'

        last_session_id = quizdatabase.get_last_session_id()

        self.assertEqual(last_session_id, expected)


    def test_get_results_by_session(self):
        timestamp_start = 1234
        timestamp_end = 5678
        user_answer = 'This is an answer'
        points = 3
        is_correct = 1
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 1234, question_id)
        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 1234, question_id)
        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 5678, question_id)

        empty_list = []

        results = quizdatabase.get_results_by_session(1234)
        self.assertNotEqual(results, empty_list)


    def test_get_results_by_invalid_session_raises_QuizDBError(self):
        timestamp_start = 1234
        timestamp_end = 5678
        user_answer = 'This is an answer'
        points = 3
        is_correct = 1
        question_id = 1

        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 1234, question_id)
        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 1234, question_id)
        quizdatabase.create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, 5678, question_id)

        with self.assertRaises(QuizDBError):
            results = quizdatabase.get_results_by_session('This is an invalid session')


    def test_get_results_when_no_results_in_db_raises_QuizDBError(self):
        with self.assertRaises(QuizDBError):
            results = quizdatabase.get_results_by_session(12345)


if __name__ == '__main__':
    unittest.main()