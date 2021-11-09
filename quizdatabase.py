from peewee import *

db = SqliteDatabase('quiz.db')

class Question(Model):
    question = CharField(null=False)
    answercorrect = CharField(null=False)
    answerincorrecta = CharField(null=False)
    answerincorrectb = CharField(null=False)
    answerincorrectc = CharField(null=False)
    # Using 1 <= difficulty makes the intent clearer. The lowest bound is 1 so having a 1 in the condition helps understand
    # Since SQLite doesn't enforce data types, do you think 0 < difficulty AND difficulty < 6 would permit 
    # a difficulty of 0.5, or 5.2? 
    difficulty = IntegerField(null=False, constraints=[Check('1 <= difficulty AND difficulty <= 5')])
    # Same comment here
    points = IntegerField(null=False, constraints=[Check('1 <= points AND points <= 100')])
    category = CharField(null=False)

    class Meta: 
        database = db

    # A Peewee model is a Python class and you can add your own methods,
    def all_answers(self):
        return [self.answercorrect, self.answerincorrecta, self.answerincorrectb, self.answerincorrectc] 

    def __str__(self):
        question_info = f'ID. {self.id} Difficulty: {self.difficulty}, Points: {self.points}, Category: {self.category}'
        question_and_answers = f'Q: {self.question}, A: {self.answercorrect}; {self.answerincorrecta}; {self.answerincorrectb}; {self.answerincorrectc}'
        return f'{question_info}\n{question_and_answers}\n'


class Result(Model):
    timestampstart = IntegerField(null=False)
    timestampend = IntegerField(null=False)
    useranswer = CharField(null=False)
    points = IntegerField(null=False)
    # Or use a BooleanField
    iscorrect = IntegerField(null=False, default=0, constraints=[Check('iscorrect IN (0, 1)')])
    sessionid = CharField(null=False)
    questionid = ForeignKeyField(Question)

    class Meta: 
        database = db

    def __str__(self):
        question_info = f'{self.id}. Session: {self.sessionid}, Question ID: {self.questionid}, Time: {self.timestampstart} to {self.timestampend}'
        user_answer_info = f'User Answer: {self.useranswer}, Points Earned: {self.pointsearned}'
        if (self.iscorrect == 0):
            is_correct_string = 'No'
        else:
            is_correct_string = 'Yes'
        return f'{question_info}\n{user_answer_info}, Correct: {is_correct_string}.\n'


class QuizDBError(Exception):
    """Custom exception primarily used to prevent empty lists & null values from being returned."""
    pass


def create_table():
    """Create Question and Result tables."""
    db.create_tables([Question, Result])


def get_all_questions():
    """Select all questions from the question table.
    Put each question in a list, then return that list."""
    questions = Question.select()
    questions_list = []
    for question in questions:
        questions_list.append(question)
    
    if not questions_list:
        raise QuizDBError(f'Error: There are no questions in the database.')

    return questions_list


def get_category_list():
    """Select all questions from the question table.
    Put each question category into a set to eliminate duplicates,
    then into a list for indexing. Return that list."""
    
    # The DB can do much of this work for you with a distinct query, for example,
    question_topics = Question.select(Question.category).distinct()

    
    questions = Question.select()     
    categories_set = set()
    for question in questions:
        categories_set.add(question.category)
    categories_list = []
    for category in categories_set:
        categories_list.append(category)

    if not categories_list:
        raise QuizDBError(f'Error: There are no categories in the database.')

    return categories_list


# def get_questions_by_category(category, max_questions):  # how many questions to return?
def get_questions_by_category(category):  # how many questions to return?
    """Select all questions under a category from the Question table.
    Put each question in a list, then return that list."""

    # since the program may ask fewer questions than available, 
    # consider using limit to return up to the max number of questions
    # save slicing lists in quiz_runner etc.
    # questions = Question.select().where(Question.category == category).limit(max_questions).execute()

    questions = Question.select().where(Question.category == category).execute()

    questions_list = []
    for question in questions:
        questions_list.append(question)

    if not questions_list:
        raise QuizDBError(f'Error: There are no questions with category: {category} in the database.')

    return questions_list


def get_question_by_id(question_id):
    """Select one question from the question table
    Return question or raise error if question not found."""

    question = Question.get_or_none(id=question_id)

    if not question:
        raise QuizDBError(f'Error: Unable to get question with id {question_id} from database.')

    return question


def convert_is_correct_to_number(is_correct):
    """Makes sure is_correct is a number since we are using sqlite for this module.
    This way it can be a boolean in the rest of the program.
    Raises error if unexpected value"""

    # This type of function is fairly common in Python since it's flexible with types and we 
    # may need to ensure a variable is a specific type.
    # Suggest using a Boolean column in the database. SQLite will convert to 1 and 0 when it stores the 
    # data and peewee will convert back to booleans for Python. 
    # Also note that 0 is "Falsy" in Python and 1 (and any other non-zero) number is truthy, but it's 
    # usually better to be consistent with the data types used to represent concepts like answer right/wrong. 

    #     number = 1
    #     if number:
    #        print('true')   # this prints if number is non-zero
    #     else:
    #        print('false')  # this prints if number is 0

    is_correct_number = 0

    if (is_correct == True):
        is_correct_number = 1
    elif (is_correct == 1):
        is_correct_number = 1
    elif (is_correct == False):
        is_correct_number = 0
    elif (is_correct == 0):
        is_correct_number = 0
    else:
        raise QuizDBError(f'Error: Cannot use {is_correct} as a value to determine whether user got question correct.')
    
    return is_correct_number


def create_question_result(timestamp_start, timestamp_end, user_answer, points, is_correct, session_id, question_id):
    """Create a new question result, then save that result to the Result table."""
    is_correct_number = convert_is_correct_to_number(is_correct)

    result = Result(timestampstart = timestamp_start, timestampend = timestamp_end, useranswer = user_answer, points=points, iscorrect = is_correct_number, sessionid = session_id, questionid = question_id)
    result.save()


def get_last_session_id():
    """Gets all results in descending order by most recent timestamp.
    Selects the first result from that list, and takes the session ID from that result. 
    Returns session ID."""

    # Good for a local SQLite database used by one person.  How would this handle a SQLServer database 
    # with multiple users and multiple attempts, perhaps attempted simultaneously?


    # If you expect 1 or 0 results, you can also use get() to get the matching object (not a list) or an Exception
    # https://docs.peewee-orm.com/en/latest/peewee/api.html?highlight=get#Model.get
    results = Result.select().order_by(Result.timestampend.desc())

    if not results:
        raise QuizDBError(f'Error: There are no results saved in the database.')

    first_result = results[0]
    session_id = first_result.sessionid
    return session_id
    

def get_results_by_session(session_id):
    """Select all results by session id from the Result table.
    Put each result in a list, then return that list."""
    results = Result.select().where(Result.sessionid == session_id)
    results_list = []
    for result in results:
        results_list.append(result)

    if not results:
        raise QuizDBError(f'Error: There are no results saved in the database for session id: {session_id}.')

    return results_list