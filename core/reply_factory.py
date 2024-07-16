
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    question = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = question['correct_answer']

    # Validate the answer
    if answer.strip().lower() == correct_answer.strip().lower():
        # Store the answer in session or database as needed
        session['answers'][current_question_id] = True  # Store True for correct answer
        return True, ""
    else:
        return False, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = sum(session.get('answers', {}).values())

    # Calculate percentage score
    if total_questions > 0:
        score_percentage = (correct_answers / total_questions) * 100
    else:
        score_percentage = 0

    if score_percentage >= 70:
        result_message = f"Congratulations! You scored {score_percentage}% in the quiz. Well done!"
    elif score_percentage >= 50:
        result_message = f"You scored {score_percentage}% in the quiz. Good effort!"
    else:
        result_message = f"You scored {score_percentage}% in the quiz. You can do better next time."

    return result_message
  
