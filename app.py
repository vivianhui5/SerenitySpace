from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
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


if __name__ == '__main__':
    app.run(debug=True)
