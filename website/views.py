from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Post is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, name=current_user.first_name)
            db.session.add(new_note)
            db.session.commit()
            flash('Post created!', category='success')
    
    notes = Note.query.all()
    notes.sort(key=lambda x : x.date, reverse=True)
    notes[:20]
    print(notes)

    return render_template("home.html", user=current_user, notes=notes)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
