import ui
import quizrunner
import quizdatabase


def get_results():
    # TODO: error handling for no quiz results in db

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


def main():
    main_menu_text = """
    1. Select a category
    2. Display last quiz results
    3. Quit
    """

    quizdatabase.create_table()

    ui.instructions()

    while True: 
        print(main_menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            # get the list of categories to display, then display them
            category_list = quizdatabase.get_category_list()
            category_string = ui.display_formatted_list(category_list)

            # get category selection, questions in that category, and number of questions desired
            category_selection = ui.select_category(category_list, category_string)
            category_questions = quizdatabase.get_questions_by_category(category_selection)
            number_of_questions = ui.select_number_of_questions(category_selection, category_questions)
            
            # run quiz with the selected category and number of questions
            quizrunner.start_quiz(category_questions, number_of_questions)

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


if __name__ == '__main__':
    main()