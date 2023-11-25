from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for


app = Flask(__name__)

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)



class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text)

    
with app.app_context():
    db.create_all()


@app.route('/')
def loading():
    return render_template('loading.html')


@app.route('/homepage')
def index():
    return render_template('index.html')

@app.route('/calming-exercises')
def calming_exercises():
    return render_template('calming-exercises.html')
    
@app.route('/educational-resources')
def educational_resources():
    return render_template('educational-resources.html')

@app.route('/hotlines')
def hotlines():
    return render_template('hotlines.html')

@app.route('/breathing')
def breathing():
    return render_template('breathing.html')

@app.route('/grounding')
def grounding():
    return render_template('grounding.html')

@app.route('/journaling')
def journaling():
    return render_template('journaling.html')

@app.route('/doodling')
def doodling():
    return render_template('doodling.html')

@app.route('/submit_journal', methods=['POST'])
def submit_journal():
    entry_text = request.form['journalEntry']
    new_entry = JournalEntry(entry=entry_text)
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('journal_board'))

@app.route('/journal-board')
def journal_board():
    entries = JournalEntry.query.order_by(JournalEntry.id.desc()).all()
    return render_template('journal-board.html', entries=entries)


@app.route('/delete_journal/<int:entry_id>', methods=['POST'])
def delete_journal(entry_id):
    entry_to_delete = JournalEntry.query.get_or_404(entry_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for('journal_board'))




if __name__ == '__main__':
    app.run(debug=True)
