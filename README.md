# Paws For Alarm

![alt text](pfareadme.jpg)

## Description

Paws For Alarm consolidates listings for animals at risk of euthanasia. As a secondary goal, it endorses animals in need of foster homes. <br>
The app supports manual entry by an admin, but primarily sources information from the RescueGroups.org API.<br>
PFA has an interface to support adding new animals and updating information each time data is ingested from external sources.<br>
![alt text](pfareadme4.jpg) <br>
Users can view all available animals, or filter results (by species, location, and organizational group).<br>
The dropdown on the species filter leverages a query and fields are dynamically updated based on the species that are in the database.<br>

![alt text](pfareadme5.jpg) <br>

Within each animal detail page, there are Bootstrap element tabs to separate the appropriate data. <br>
![alt text](pfareadme3.jpg) <br>
<br>

## Admin Routes

Both admin routes have client and server side validation.<br>
A notable feature of the add animal route is the ability for the admin to search for a shelter in the database without leaving the page.<br>
An AJAX request is made which returns JSON data and updates the DOM- in this case, the dropdown menu.<br><br>

## Technologies Used

Python<br>
Flask<br>
PostgreSQL<br>
SQLAlchemy<br>
Jinja <br>
HTML<br>
CSS<br>
JavaScript<br>
AJAX<br>
JSON<br>
Bootstrap<br>

## Setup

Create a virtual environment. <br>
Install the items in requirements.txt <br>
You will need to request an API key from RescueGroups.org.<br>
To use the manual entry features, you'll need to generate an authentication token.<br>
Additionally, a password is used for code implemented to prevent CSRF attacks- this will need to be generated.<br><br>
Run seed.py and rescueorg.py <br>

## Reminders after changes to model.py

Make changes to forms.py (in the case of changing data type)<br>
Run seed.py <br>
Run rescueorg.py <br>
Confirm local behavior <br>
Deploy changes to server <br>
Note that you may need to stop flask using "sudo systemctl stop flask"

## Running locally

Source your secrets file <br>
`source secrets.sh`

Activate virtual environment <br>
`source env/bin/activate`

Run server file <br>
` python3 server.py`

## Creator Credit<br>

Unsplash images were used to replace shelter animal images for the README file.<br>
Thank you to the following unsplash photographers.<br>
@lacellia<br>
@e_d_g_a_r<br>
@marliesestreefland<br>
