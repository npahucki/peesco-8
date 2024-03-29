# -*- coding: utf-8 -*-
from bartendro import app, db
from flask import Flask, request, jsonify
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm

@app.route('/ws/booze/match/<str>')
def ws_booze(request, str):
    str = str + "%%"
    boozes = db.session.query("id", "name").from_statement("SELECT id, name FROM booze WHERE name LIKE :s").params(s=str).all()
    return jsonify(boozes)



@app.route('/ws/booze/all')
def ws_booze_all():
    boozes = db.session.query("id", "desc").from_statement("SELECT * FROM Drink")
    print boozes
    
    # 	boozes = db.session.query(Drink).order_by(Drink.id).all()
    return jsonify(boozes)
	
	
    
    
