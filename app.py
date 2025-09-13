from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    notes = Note.query.order_by(Note.position).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['note']
    max_position = db.session.query(db.func.max(Note.position)).scalar() or 0
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_note = Note(content=content, position=max_position + 1, timestamp=timestamp)
    db.session.add(new_note)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

@app.route('/reorder', methods=['POST'])
def reorder():
    order = request.json['order']
    for idx, note_id in enumerate(order):
        note = Note.query.get(note_id)
        note.position = idx
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
