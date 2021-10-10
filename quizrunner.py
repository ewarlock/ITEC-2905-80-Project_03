
from random import shuffle
import datetime


def shuffle_list(shuffle_list):
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


def grade_question(correct_answer, user_answer):
    """Returns whether or not question correct.
    Returns True for correct.
    Returns False for incorrect."""
    if (correct_answer == user_answer):
        print(f'You selected {user_answer}.\nThat\'s Correct!\n')
        return True
    else:
        print(f'You selected {user_answer}.\nThat is incorrect, sorry!\nThe correct answer is {correct_answer}.\n')
        return False


def calculate_total_score(results):
    """Returns total score for a session based on results from that session and whether or not result was correct."""
    total_score = 0
    for result in results:
        if (result.iscorrect == 1):
            total_score += result.points
    return total_score


def calculate_total_available_points(results):
    """Returns total available points for a session based on results from that session.
    This is the maximum possible score for a user to get on the quiz given during that session."""
    available_points = 0
    for result in results:
        available_points += result.points
    return available_points


def calculate_score_percentage(total_score, available_points):
    """Takes the user's score and the maximum possible score and returns the percentage the user got correct."""
    percentage = (total_score / available_points) * 100
    return percentage


def get_timestamp():
    """Returns a current timestamp."""
    time = datetime.datetime.now()
    timestamp = time.timestamp()
    return timestamp


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


