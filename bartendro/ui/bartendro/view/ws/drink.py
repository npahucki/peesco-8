# -*- coding: utf-8 -*-
from time import sleep
from bartendro import app, db
from flask import Flask, request, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import ServiceUnavailable
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm
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
    
    
    
    
    
    
    
    
    
    
    
    
    