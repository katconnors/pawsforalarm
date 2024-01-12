
from flask import Flask, render_template, request, redirect
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

@app.route('/faq')
def faq():

    return render_template('faq.html')

@app.route('/add', methods=['GET','POST'])
def add_entry():

    name = request.form.get('name')
    type = request.form.get('type')
    breed = request.form.get('breed')
    age = request.form.get('age')
    gender = request.form.get('gender')
    code = request.form.get('code')
    source = request.form.get('source')
    shelterid = request.form.get('shelter')
    url = request.form.get('url')
    joindate = request.form.get('joindate')
    weight = request.form.get('weight')
    euthdate = request.form.get('euthdate')
    bio = request.form.get('bio')

    shelter = crud.specific_shelter(shelterid)

    if request.method=='POST':
        crud.create_animal(name,type,breed,age,gender,code,source,shelter,url,joindate,weight,euthdate,bio)
        return redirect("/confirm")


    else:
        return render_template('add_entry.html')
    

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')






if __name__ == "__main__":

    database_connect(app,"pawsforalarm")

    #important to disable debug later
    app.run(debug=True,host="0.0.0.0")