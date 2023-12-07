from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Configure database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Database model for journal entries
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text)

# Database model for doodle entries
class DoodleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)  

# Create database tables
with app.app_context():
    db.create_all()

# Route for the home page
@app.route('/')
def loading():
    return render_template('loading.html')

# Additional routes for various pages
@app.route('/homepage')
def index():
    return render_template('index.html')

@app.route('/educational-resources')
def educational_resources():
    return render_template('educational-resources.html')

@app.route('/breathing')
def breathing():
    return render_template('breathing.html')

# Route for grounding page, handling both GET and POST
@app.route('/grounding', methods=["GET", "POST"])
def grounding():
    if request.method == "POST":
        # Process form data on POST request
        response1 = request.form.get("see")
        response2 = request.form.get("touch")
        response3 = request.form.get("hear")
        response4 = request.form.get("smell")
        response5 = request.form.get("taste")
        # Render response template with form data
        return render_template("grounded.html", response1=response1, response2=response2, response3=response3, response4=response4, response5=response5)
    else:
        return render_template('grounding.html')

# Journaling page route
@app.route('/journaling')
def journaling():
    return render_template('journaling.html')

# Route to handle journal entry submission
@app.route('/submit_journal', methods=['POST'])
def submit_journal():
    entry_text = request.form['journalEntry']
    new_entry = JournalEntry(entry=entry_text)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('journal_board'))

# Display journal entries
@app.route('/journal-board')
def journal_board():
    entries = JournalEntry.query.order_by(JournalEntry.id.desc()).all()
    return render_template('journal-board.html', entries=entries)

# Route to delete a journal entry
@app.route('/delete_journal/<int:entry_id>', methods=['POST'])
def delete_journal(entry_id):
    entry_to_delete = JournalEntry.query.get_or_404(entry_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for('journal_board'))

# Doodling page route
@app.route('/doodling')
def doodling():
    return render_template('doodling.html')

# Route to handle doodle submission
@app.route('/submit_doodle', methods=['POST'])
def submit_doodle():
    doodle_data = request.form['doodleData']
    new_doodle = DoodleEntry(data=doodle_data)
    db.session.add(new_doodle)
    db.session.commit()
    return redirect(url_for('sketches'))

# Display doodle entries
@app.route('/sketches')
def sketches():
    doodles = DoodleEntry.query.order_by(DoodleEntry.id.desc()).all()
    return render_template('sketches.html', doodles=doodles)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
