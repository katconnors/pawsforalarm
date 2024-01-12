
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

    type = request.args.get('type')
    state = request.args.get('state')

    
    animals = crud.view_animals(type,state)


    return render_template('animals.html',animals=animals,type=type,state=state)


@app.route('/animals/<id>')
def animal(id):

    animal = crud.specific_animal(id)
    return render_template('animal_detail.html',animal=animal)





if __name__ == "__main__":

    database_connect(app,"pawsforalarm")

    #important to disable debug later
    app.run(debug=True,host="0.0.0.0")