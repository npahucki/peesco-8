# -*- coding: utf-8 -*-
from time import sleep
from bartendro import app, db
from flask import Flask, request, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import ServiceUnavailable
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm
from bartendro.model.drink_name import DrinkName
from bartendro import constant

import json

@app.route('/ws/drink/<int:drink>')
def ws_drink(drink):
    mixer = app.mixer

    if app.options.must_login_to_dispense and not current_user.is_authenticated():
        return "login required"

    recipe = {}
    for arg in request.args:
        recipe[arg] = int(request.args.get(arg))

    if mixer.make_drink(drink, recipe):
        return "ok\n"
    else:
        raise ServiceUnavailable("Error: %s (%d)" % (mixer.get_error(), ret))

@app.route('/ws/drink/<int:drink>/available/<int:state>')
def ws_drink_available(drink, state):

    if not drink:
        db.session.query(Drink).update({'available' : state})
    else:
        db.session.query(Drink).filter(Drink.id==drink).update({'available' : state})
    db.session.flush()
    db.session.commit()
    return "ok\n"


@app.route('/ws/drink/all')
def ws_drink_all():
    
    drinks = db.session.query(Drink).order_by(Drink.id).all()
    listDrinks = []

    for drink in drinks:
        listDrinks.append({ 'desc' : drink.desc.encode('utf8'),
                            'id' : drink.id, 
                            'name_id' : drink.name_id, 
                            'sugg_size' : drink.sugg_size, 
                            'popular' : drink.popular,
                            'available' : drink.available 
                            })
    return jsonify(DrinkList=listDrinks)    
    

def process_ingredients(drinks):
    for drink in drinks:
        drink.process_ingredients()

def filter_drink_list(can_make_dict, drinks):
    filtered = []
    for drink in drinks:
        try:
            foo =can_make_dict[drink.id]
            filtered.append(drink)
        except KeyError:
            pass
    return filtered
 
@app.route('/ws/drink/dindex')
def ws_index():

#     if app.mixer.disp_count == 1:
#         disp = db.session.query(Dispenser) \
#                           .filter(Dispenser.id == 1) \
#                           .one()
#         return render_template("shotbot", booze=disp.booze.name, title="ShotBot")

    can_make = app.mixer.get_available_drink_list()
    can_make_dict = {}
    for drink in can_make:
        can_make_dict[drink] = 1

    top_drinks = db.session.query(Drink) \
                        .join(DrinkName) \
                        .filter(Drink.name_id == DrinkName.id)  \
                        .filter(Drink.popular == 1)  \
                        .filter(Drink.available == 1)  \
                        .order_by(DrinkName.name).all() 
    top_drinks = filter_drink_list(can_make_dict, top_drinks)
    process_ingredients(top_drinks)

    other_drinks = db.session.query(Drink) \
                        .join(DrinkName) \
                        .filter(Drink.name_id == DrinkName.id)  \
                        .filter(Drink.popular == 0)  \
                        .filter(Drink.available == 1)  \
                        .order_by(DrinkName.name).all() 
    other_drinks = filter_drink_list(can_make_dict, other_drinks)
    process_ingredients(other_drinks)


    topDrinks = []

    for drink in top_drinks:
        topDrinks.append({ 'desc' : drink.desc.encode('utf8'),
                            'id' : drink.id, 
                            'name' : drink.name.name
                            })
                            
    otherDrinks = []

    for drink in other_drinks:
        otherDrinks.append({ 'desc' : drink.desc.encode('utf8'),
                            'id' : drink.id, 
                            'name' : drink.name.name
                            })
                                                    
#     allDrinks = []
#     allDrinks.append(['topDrinks', topDrinks])
#     allDrinks.append(['otherDrinks', otherDrinks])    

    allDrinks = []
    allDrinks.append(['topDrinks', topDrinks])
    allDrinks.append(['otherDrinks', otherDrinks])    


    
    return jsonify(AllDrinks=[{'topDrinks':topDrinks}, {'otherDrinks':otherDrinks}])    




            
#     return render_template("index", 
#                            top_drinks=top_drinks, 
#                            other_drinks=other_drinks,
#                            title="Bartendro")

    
    
    
    
    
    
    
    
    
    
    