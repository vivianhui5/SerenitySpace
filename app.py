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
