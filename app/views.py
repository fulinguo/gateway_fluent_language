from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models.user import Conversation, User
from . import db
import json
from .utils.openai_funcs import example_prompt, generate_system_message, get_response, related_prompt
from .utils.organize_notes_gpt import get_notes

views = Blueprint('views', __name__)

temperature = 0.7
model = "gpt-3.5-turbo-1106"
obj_language, answer_language = 'English', 'Chinese'

@views.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    user_logged_in = 'user_id' in session  # Check if user is logged in

    if request.method == 'POST':
        question = request.form['question']
        # Assuming process_question is a function that handles the question
        # answer = process_question(question)

    return render_template('index.html', answer=answer, user_logged_in=user_logged_in)

@views.route('/change_language', methods=['POST'])
@login_required
def change_language():
    new_language = request.form['language']
    
    # Update the user's preferred language in the database
    if current_user.is_authenticated:
        current_user.preferred_answer_language = new_language
        db.session.commit()
        flash('Language updated successfully.')
    else:
        flash('User not found.')

    return redirect(url_for('views.dashboard'))

'''
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)
'''

@views.route('/get-answer', methods=['POST'])
def get_answer():
    system_message = generate_system_message(obj_language, answer_language)
    question = request.form.get('question')
    
    if 'message_list' not in session:
        session['message_list'] = [{"role": "system", "content": system_message}]
        
    session['message_list'].append({"role": "user", "content": question})
    answer = get_response(session['message_list'], temperature, model)
    session['message_list'].append({"role": "assistant", "content": answer})

    print(session['message_list'])
    
    return jsonify({'answer': answer})

@views.route('/get-examples', methods=['POST'])
def get_examples():
    session['message_list'].append({"role": "user", "content": example_prompt})
    answer = get_response(session['message_list'], temperature, model)
    session['message_list'].append({"role": "assistant", "content": answer})
    
    return jsonify({'answer': answer})

@views.route('/get-related', methods=['POST'])
def get_related():
    session['message_list'].append({"role": "user", "content": related_prompt})
    answer = get_response(session['message_list'], temperature, model)
    session['message_list'].append({"role": "assistant", "content": answer})
    
    return jsonify({'answer': answer})


@views.route('/notes')
def notes_page():
    user_logged_in = 'message_list' in session
    if user_logged_in:
        print(session['message_list'])
        notes = get_notes(obj_language, answer_language, session['message_list'], temperature, model)
        print(notes)
        return render_template('notes.html', notes=notes)
    else:
        return redirect(url_for('auth.login'))  # Redirect to login if user not logged in

@views.route('/tests')
def tests_page():
    user_logged_in = 'user_id' in session
    if user_logged_in:
        return render_template('tests.html')
    else:
        return redirect(url_for('auth.login'))
    

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Conversation.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
