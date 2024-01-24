
from flask import Flask, render_template, request, redirect
from model import database_connect
import crud
from jinja2 import StrictUndefined
import os


app = Flask(__name__)
API = os.environ['API_KEY']

#information endpoints
@app.route('/')
def home():
    """Homepage for Paws for Alarm"""

    return render_template('homepage.html')

@app.route('/faq')
def faq():
    """Frequently Asked Questions"""

    return render_template('faq.html')


#animal endpoints
@app.route('/animals')
def animals():
    """Shows all animals at risk, with type and state filters at top of page
    Also includes sorting functionality"""

    type = request.args.get('type')
    state = request.args.get('state')
    sort_type = request.args.get('sort-type')
    

    animals = crud.view_animals(type,state,sort_type)


    return render_template('animals.html',animals=animals,type=type,state=state,sort_type=sort_type)


@app.route('/animals/<id>')
def animal(id):
    """Animal detail page"""

    animal = crud.specific_animal(id)
    return render_template('animal_detail.html',animal=animal)


#admin entry endpoints
@app.route("/sheltername")
def get_sheltername():
    """Obtain shelter name"""
    typed_text = request.args.get("shelter-name")

    suggested_shelters = crud.give_shelter_names(typed_text)

    return {
        "success": True,
        "shelters": suggested_shelters}



@app.route('/add', methods=['GET','POST'])
def add_entry():
    """Page for admin to manually add animals"""
    #note that this will currently default to None for api_id
    api_id = request.form.get('api-id') if request.form.get('api-id') else None
    name = request.form.get('name')
    image = request.form.get('image')
    type = request.form.get('type')
    breed = request.form.get('breed')
    age = request.form.get('age') if request.form.get('age') else None
    gender = request.form.get('gender')
    code = request.form.get('code')
    source = request.form.get('source')
    shelterid = request.form.get('shelter')
    url = request.form.get('url')
    joindate = request.form.get('joindate') if request.form.get('joindate') else None
    weight = request.form.get('weight') if request.form.get('weight') else None
    euthdate = request.form.get('euthdate') if request.form.get('euthdate') else None
    bio = request.form.get('bio') if request.form.get('bio') else None
    auth = request.form.get('auth-code') 

    shelter = crud.specific_shelter(shelterid)


    #checks for correct authentication token
    if request.method=='POST' and auth== os.environ["password"]:
    
        crud.create_animal(api_id,name,image,type,breed,gender,code,source,shelter,url,age,joindate,weight,euthdate,bio)
        return redirect("/confirm")

    else:
        return render_template('add_entry.html',auth=auth)
    

    
@app.route('/addshelter',methods=['GET','POST'])
def add_shelter():
    """Page for admin to manually add shelters"""

    name = request.form.get('name')
    address = request.form.get('address')
    city = request.form.get('city')
    state_input = request.form.get('state')
    #including to prevent inconsistencies in state result capitalization for filter functionality
    if state_input !=None:
        state = state_input.upper()
    zipcode = request.form.get('zipcode')
    website = request.form.get('website')
    auth = request.form.get('auth-code') 

    #checks for correct authentication token

    if request.method=='POST' and auth== os.environ["password"]:
        crud.create_shelter(name,address,city,state,zipcode,website)
        return redirect("/confirm")

    else:
        return render_template('add_shelter.html',auth=auth)
    
    

@app.route('/confirm')
def confirm():
    """Page that appears after a successful shelter or animal entry"""

    return render_template('confirm.html')




if __name__ == "__main__":

    database_connect(app,"pawsforalarm")

    #important to disable debug later

    app.run(debug=True,host="0.0.0.0")