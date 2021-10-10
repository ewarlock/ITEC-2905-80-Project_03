
import validation


def instructions():
    instructions = """
    Welcome to the quiz program! Please type 1 to start quiz, then select a category. 
    Once you have selected a category, enter the number of questions you'd like to be asked.
    During the quiz, please type A, B, C or D to select an answer for each question. At the end of the quiz, the results will be displayed.
    You can also display the results from the previous session before selecting a category.
    """

    return instructions


def format_list(unformatted_list):
    """Take a list and display it as a numbered list using item index + 1."""
    list_string = ''
    for item in unformatted_list:
        index = unformatted_list.index(item)
        index += 1
        list_string += f'{index}. {item}\n'

    return(list_string)


def select_category(category_list, category_string):
    """Take the list of categories, and allow the user to select a category. Return that category."""
    while True:
        print(category_string)
        index = input('Type the number of the category you want to be quizzed on: ')
        if validation.is_number(index) == False:
            print('\nPlease enter a numeric value.\n')
        elif validation.is_in_range(index, category_list) == False:
            print('\nPlease select a category in the category list, by number.\n')
        else:
            category = category_list[int(index) -1]
            return category


def select_number_of_questions(category, category_questions):
    """Return the number of questions desired by the user, making sure the number is within the correct range based on their selected category."""
    while True:
        print(f'{len(category_questions)} questions available in {category}.')
        number_of_questions_string = input(f'Type in the number of questions you want to be quizzed on: ')
        if validation.is_number(number_of_questions_string) == False:
            print('\nPlease enter a numeric value.\n')
        elif validation.is_in_range(number_of_questions_string, category_questions) == False:
            print(f'\nPlease enter a number within the range provided for {category}.\n')
        else:
            number_of_questions = int(number_of_questions_string)
            return number_of_questions


def format_quiz_question(question):
    """Returns a formatted question for the user."""
    question_string = f'Question: {question.question}\n'
    return question_string


def answer_quiz_question(question_string, answer_string, answers_list):
    """Collects user answer as index to answers list"""
    answer_prompt = 'Type the number of your chosen answer: '
    while True:
        index = input(question_string + answer_string + answer_prompt)
        if validation.is_number(index) == False:
            print('\nPlease enter a numeric value.\n')
        elif validation.is_in_range(index, answers_list) == False:
            print('\nPlease select an answer in the answers list, by number.\n')
        else:
            index = int(index) - 1
            return index


def display_results(category, score, points_available, percentage, quiz_time):
    """Display user results."""
    intro_string = 'For the most recent quiz session:\n'
    category_string = f'The quiz category was {category}.\n'
    quiz_time_string = f'The total time to take the quiz was {quiz_time:.2f} minutes.\n'
    quiz_score_string = f'{score} points were earned, out of a total of {points_available}.\n'
    quiz_score_percentage_string = f'The user got a score of {percentage:.2f}%'

    results_string = f'\n{intro_string}{category_string}{quiz_time_string}{quiz_score_string}{quiz_score_percentage_string}\n'

    return results_string