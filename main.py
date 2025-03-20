from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
@app.route('/movies')
def movies():
    df = pd.read_csv('movies.csv')
    df['poster'] = df['poster'].fillna('')
    data = df.to_dict('records')
    return render_template('movies.html', movies=data)


