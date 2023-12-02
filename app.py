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

class DoodleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)  # Stores doodle data as JSON string

def clear_doodle_entries():
    """Clear all entries in the DoodleEntry table."""
    try:
        db.session.query(DoodleEntry).delete()
        db.session.commit()
    except Exception as e:
        print("Error clearing DoodleEntry table:", e)
        db.session.rollback()

with app.app_context():
    db.create_all()
    clear_doodle_entries()  # Clear the table when the app starts


with app.app_context():
    db.create_all()


@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/homepage')
def index():
    return render_template('index.html')
    
@app.route('/educational-resources')
def educational_resources():
    return render_template('educational-resources.html')

@app.route('/breathing')
def breathing():
    return render_template('breathing.html')

@app.route('/grounding', methods=["GET", "POST"])
def grounding():
    if request.method == "POST":
        response1 = request.form.get("see")
        response2 = request.form.get("touch")
        response3 = request.form.get("hear")
        response4 = request.form.get("smell")
        response5 = request.form.get("taste")
        print(response1, response2, response3, response4, response5)
        return render_template("grounded.html", response1=response1, response2=response2, response3=response3, response4=response5, response5=response5)
    else:
        return render_template('grounding.html')

@app.route('/journaling')
def journaling():
    return render_template('journaling.html')


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

@app.route('/doodling')
def doodling():
    return render_template('doodling.html')

@app.route('/submit_doodle', methods=['POST'])
def submit_doodle():
    doodle_data = request.form['doodleData']
    new_doodle = DoodleEntry(data=doodle_data)
    db.session.add(new_doodle)
    db.session.commit()
    print("hi")
    return redirect(url_for('sketches'))


@app.route('/sketches')
def sketches():
    doodles = DoodleEntry.query.order_by(DoodleEntry.id.desc()).all()
    for doodle in doodles:
        print(doodle.id, doodle.data)  # This will print the id and the data of each doodle
    return render_template('sketches.html', doodles=doodles)


if __name__ == '__main__':
    app.run(debug=True)