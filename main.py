import ui
import quizrunner
import quizdatabase
import uuid


def main():
    main_menu_text = """
    1. Select a category
    2. Display last quiz results
    3. Quit
    """

    quizdatabase.create_table()

    ui.instructions()

    while True: 
        # main menu loop - user can return to main menu after displaying results
        # user will also be returned to main menu if their input is invalid
        print(main_menu_text)
        choice = input('Enter your choice: ')


        if choice == '1':
            # get the list of categories to display
            category_list = quizdatabase.get_category_list()
            category_string = ui.format_list(category_list)

            # get category selection, questions in that category, and number of questions desired from user input
            category_selection = ui.select_category(category_list, category_string)
            category_questions = quizdatabase.get_questions_by_category(category_selection)  # could you request only the number of questions needed?
            number_of_questions = ui.select_number_of_questions(category_selection, category_questions)

            # configure the quiz based on user's selected category & number of questions
            quiz_questions = prepare_quiz_questions(category_questions, number_of_questions)
            session_id = uuid.uuid1() # generate random session ID

            run_quiz(quiz_questions, session_id)

            # display how the user did on the quiz, then end program
            results = get_results()
            print(results)
            print('Thanks for using this program!')
            break


        elif choice == '2':
            # display how the last quiz session went, then allow user to continue program
            results = get_results()
            print(results)


        elif choice == '3':
            print('Thanks for using this program!')
            break


        else:
            print('Not a valid selection, please try again')


def run_quiz(questions, session_id):
    """Takes a list of questions based on the user's settings.
    Displays each question for the user and records the result in the database."""

    for question in questions:
        start_time = quizrunner.get_timestamp() # the time that the question is printed

        answer_list = quizrunner.create_answer_list(question)

        # in an unshuffled answer list, position 0 always contains the correct answer
        # due to the design of the questions table in the quiz database
        correct_answer = answer_list[0] # take correct answer out of unshuffled answer list for grading
        correct_answer = question.answercorrect  # the question object directly knows the correct answer too

        # shuffle quiz answers, then display them for user input
        answer_list_shuffled = quizrunner.shuffle_list(answer_list)
        question_string = ui.format_quiz_question(question)
        answer_list_string = ui.format_list(answer_list_shuffled)

        # take user's input - a number - and use it to get the answer they selected 
        # by changing it to a valid index for the shuffled answer list
        user_answer_index = ui.answer_quiz_question(question_string, answer_list_string, answer_list_shuffled)
        user_answer = answer_list_shuffled[user_answer_index]

        # grade the user's answer. if the user answered correctly, the question points are added. otherwise, 0 is added
        is_correct = quizrunner.grade_question(correct_answer, user_answer)

        end_time = quizrunner.get_timestamp() # the time after the user has answered, just before the next question is printed

        # save to the results database
        quizdatabase.create_question_result(start_time, end_time, user_answer, question.points, is_correct, session_id, question.id)


def prepare_quiz_questions(questions, number_of_questions):
    """Shuffles a list of questions, then trims the list down to the user's requested number of questions."""
    # prepare the list of questions by randomizing the list
    # then trimming the list down to the user's requested number of questions
    # see notes on requesting only the number of questions needed using a limit query in the DB
    questions_randomized = quizrunner.shuffle_list(questions)
    questions_trimmed = quizrunner.trim_list(questions_randomized, number_of_questions)

    return questions_trimmed


def get_results():
    # get the most recent session results
    last_session_id = quizdatabase.get_last_session_id()
    last_session_results = quizdatabase.get_results_by_session(last_session_id)

    # get the category using one of the questions from the last session results
    question = quizdatabase.get_question_by_id(last_session_results[0].questionid)
    last_session_category = question.category

    # get the user's score and the total points available
    score = quizrunner.calculate_total_score(last_session_results)
    points_available = quizrunner.calculate_total_available_points(last_session_results)
    percentage = quizrunner.calculate_score_percentage(score, points_available)

    # get the user's quiz time
    total_quiz_time_seconds = quizrunner.calculate_total_quiz_time(last_session_results)
    total_quiz_time_minutes = quizrunner.convert_to_minutes(total_quiz_time_seconds)

    # return a formatted string with this information
    return ui.display_results(last_session_category, score, points_available, percentage, total_quiz_time_minutes)


if __name__ == '__main__':
    main()