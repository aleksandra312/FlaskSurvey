from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask import flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = []


@app.route('/')
def return_home():
    """Returns Home Page with Survey title and instructions."""
    return render_template("home.html", survey = survey)

@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Shows Question Page."""
    if (len(RESPONSES) != question_id):
        flash(f"Invalid question: {question_id}.")
        return redirect(f"/questions/{len(RESPONSES)}")

    question = survey.questions[question_id]
    question_num = question_id
    return render_template("questions.html", question = question, number = question_num)

@app.route('/answer', methods =["POST"])
def handle_answer():
    """Saves question answer and redirects to the next question."""
    choice = request.form['answer']
    RESPONSES.append(choice)

    if (len(RESPONSES) == len(survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f"/questions/{len(RESPONSES)}")

@app.route('/complete')
def complete_survey():
    """Completion of the Survey."""
    return render_template('completion.html')




