
from flask import Flask, render_template, request
from model import database_connect, database
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')



@app.route('/animals')
def animals():

    animals = crud.view_animals()
    return render_template('animals.html',animals=animals)

# need to resolve the variable route issue
@app.route('/animals/<id>')
def animal():

    animal = crud.specific_animal()
    return render_template('animal_detail.html',animal=animal)





if __name__ == "__main__":

    
    database_connect(app,"pawsforalarm")
    #important to disable debug later
    app.run(debug=True,host="0.0.0.0")