# -*- coding: utf-8 -*-
from bartendro import app, db
from flask import Flask, request, jsonify
from flask.ext.login import current_user
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm
import time

@app.route('/ws/shotbot')
def ws_shotbot():
    print "hola"
    
    if app.options.must_login_to_dispense and not current_user.is_authenticated():
        return "login required"

    indio = app.indio
    driver = app.driver
    indio.pee()   
    time.sleep(1)
    indio.stand(55)
    time.sleep(.5)
    driver.make_shot(80)
    while driver.is_dispensing(0)[0] == True:
        print "Waiting for dispense to finish. Status:{0}".format(driver.is_dispensing(0))
    	indio.center(30,15)
        time.sleep(.75)
	indio.center(-30,15)
	time.sleep(.75)
    indio.center()
    indio.dick_shake(5, True)
    indio.side_shake(5, True)
    indio.center()
    indio.sit()


    return "ok\n"

    
    
    
    
    
    
    
    
    
    
    