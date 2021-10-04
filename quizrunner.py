
from random import shuffle
import datetime
import ui
from quizdatabase import create_question_result as save_result

import uuid

# (timestamp_start, timestamp_end, user_answer, points_earned, is_correct, session_id, question_id)
def randomize_list(shuffle_list):
    """Takes a list and randomizes it"""
    # found here https://www.programming-idioms.org/idiom/10/shuffle-a-list/182/python
    shuffle(shuffle_list)
    return shuffle_list


def trim_list(starting_list, max):
    """Takes a list and trims it based on a maximum value"""
    new_list = starting_list[:max]
    return new_list


def create_answer_list(question):
    """Returns a list based on the four potential answers for a question"""
    answer_list = []
    answer_list.append(question.answercorrect)
    answer_list.append(question.answerincorrecta)
    answer_list.append(question.answerincorrectb)
    answer_list.append(question.answerincorrectc)
    return answer_list


def get_timestamp():
    """Returns a current timestamp."""
    time = datetime.datetime.now()
    timestamp = time.timestamp()
    return timestamp


def grade_question(correct_answer, user_answer):
    """Returns whether or not question correct."""
    if (correct_answer == user_answer):
        print(f'You selected {user_answer}.\nThat\'s Correct!\n')
        return 1
    else:
        print(f'You selected {user_answer}.\nThat is incorrect, sorry!\nThe correct answer is {correct_answer}.\n')
        return 0


def calculate_total_score(results):
    """Returns total score for a session based on results from that session and whether or not result was correct."""
    total_score = 0
    for result in results:
        if (result.iscorrect == 1):
            total_score += result.points
    return total_score


def calculate_total_available_points(results):
    """Returns total available points for a session based on results from that session."""
    available_points = 0
    for result in results:
        available_points += result.points
    return available_points


def calculate_score_percentage(total_score, available_points):
    percentage = (total_score / available_points) * 100
    return percentage


def calculate_total_question_time(result):
    """Returns the total time in seconds for a single quiz result."""
    total_time = result.timestampend - result.timestampstart
    return total_time


def calculate_total_quiz_time(results):
    """Returns the total time in seconds for a list of quiz results."""
    total_time = 0
    for result in results:
        total_time += calculate_total_question_time(result)
    return total_time


def convert_to_minutes(timestamp):
    """Puts seconds into minutes."""
    minutes = timestamp / 60
    return minutes


def start_quiz(questions, number_of_questions):
    # TODO: refactor? - feel like some of this needs to be put into smaller functions
    # while some can be done by main.py...
    # TODO: find a better name for this module - it doesn't just run the quiz !!!!

    # prepare the list of questions by randomizing the list
    # then trimming the list down to the user's requested number of questions
    questions_randomized = randomize_list(questions)
    questions_trimmed = trim_list(questions_randomized, number_of_questions)

    session_id = uuid.uuid1() # generate random session ID

    for question in questions_trimmed:
        start_time = get_timestamp() # the time that the question is printed

        answer_list = create_answer_list(question)
        correct_answer = answer_list[0]

        # shuffle quiz answers, then display them for user input
        answer_list_randomized = randomize_list(answer_list)

        question_string = ui.format_quiz_question(question)
        answer_list_string = ui.display_formatted_list(answer_list_randomized)

        # take user's input - a number - and use it to get the answer they selected
        user_answer_index = ui.answer_quiz_question(question_string, answer_list_string, answer_list_randomized)
        user_answer = answer_list_randomized[user_answer_index]

        # grade the user's answer. if the user answered correctly, the question points are added. otherwise, 0 is added.
        is_correct = grade_question(correct_answer, user_answer)

        end_time = get_timestamp() # the time after the user has answered, just before the next question is printed

        # save this to the results database
        save_result(start_time, end_time, user_answer, question.points, is_correct, session_id, question.id)