
from flask import Flask, render_template, request, redirect
from model import database_connect
import crud
from jinja2 import StrictUndefined
import os
import forms


app = Flask(__name__)
API = os.environ['API_KEY']
app.secret_key = os.environ['SECRET_KEY']

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
    query_state = request.args.get('state')
    group = request.args.get('fosteuthselection')
    sort_type = request.args.get('sort-type',"scheduled_euthanasia_date")

    

    animals = crud.view_animals(type,query_state,group,sort_type)
    state_list = crud.shelter_state_list()
    animal_list = crud.animal_type_list()


    return render_template('animals.html',animals=animals,state_list=state_list,animal_list=animal_list,group=group,type=type,query_state=query_state,sort_type=sort_type)


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

    #status and source should not be altered
    status = "available"
    source = "admin"
    

    #note that this will currently default to None for api_id
    api_id = None

    shelterid = request.form.get('shelter')

    shelter = crud.specific_shelter(shelterid)
    

    #data validation

    form = forms.AnimalForm(request.form)
    
    
    if form.validate_on_submit():

        name = form.name.data
        url = form.url.data
        image = form.image.data
        type= form.type.data
        gender = form.gender.data
        breed = form.breed.data
        age = form.age.data
        available_date = form.availabledate.data
        euthdate = form.euthdate.data
        groupstatus = form.groupstatus.data
        joindate = form.joindate.data
        code = form.code.data
        weight= form.weight.data
        bio = form.bio.data

    
        crud.create_animal(api_id,name,image,type,breed,gender,code,source,shelter,available_date,groupstatus,status,url,age,joindate,weight,euthdate,bio)
        return redirect("/confirm")

    else:
        return render_template('add_entry.html',form=form)
    

    
@app.route('/addshelter',methods=['GET','POST'])
def add_shelter():
    """Page for admin to manually add shelters"""

    #source should not be altered
    source = "admin"

    form = forms.ShelterForm(request.form)

    if form.validate_on_submit():

        name = form.name.data
        streetaddress = form.streetaddress.data
        city = form.city.data
        #including to prevent inconsistencies in state result capitalization for filter functionality
        state = form.state.data.upper()
        zipcode = form.zipcode.data
        website = form.website.data

    
        crud.create_shelter(name,streetaddress,city,state,zipcode,website,source)
        return redirect("/confirm")

    else:
        return render_template('add_shelter.html',form=form)
    
    

@app.route('/confirm')
def confirm():
    """Page that appears after a successful shelter or animal entry"""

    return render_template('confirm.html')




if __name__ == "__main__":

    database_connect(app,"pawsforalarm")

    #important to disable debug later

    app.run(debug=True,host="0.0.0.0")