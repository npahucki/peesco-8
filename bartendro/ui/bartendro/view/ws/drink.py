# -*- coding: utf-8 -*-
from time import sleep
import math
from bartendro import app, db
from flask import Flask, request, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.exceptions import ServiceUnavailable
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.model.drink_booze import DrinkBooze
from bartendro.model.booze import BOOZE_TYPE_UNKNOWN, BOOZE_TYPE_ALCOHOL, BOOZE_TYPE_TART, BOOZE_TYPE_SWEET
from bartendro.form.booze import BoozeForm
from bartendro.model.drink_name import DrinkName
from bartendro import constant

import json

# @app.route('/ws/drink/<int:drink>')
# def ws_drink(drink):
#     mixer = app.mixer
# 
#     if app.options.must_login_to_dispense and not current_user.is_authenticated():
#         return "login required"
# 
#     recipe = {}
#     for arg in request.args:
#         recipe[arg] = int(request.args.get(arg))
# 
#     if mixer.make_drink(drink, recipe):
#         return "ok\n"
#     else:
#         raise ServiceUnavailable("Error: %s (%d)" % (mixer.get_error(), ret))

@app.route('/ws/drink/<int:drink>')
def ws_drink(drink):
    mixer = app.mixer
    print "El request viene con la cantidad de args: " , len(request.args)
    if app.options.must_login_to_dispense and not current_user.is_authenticated():
        return "login required"

    recipe = {}
    
    if len(request.args) == 0:
    	print "NO HAY ARGS"
    	recipe = getRecipeFromDrink(drink,150)
    	print "NO ARGS, LA RECETA: ", recipe
    	
    else:
      for arg in request.args:
        recipe[arg] = int(request.args.get(arg))
        print recipe
      
      

    if mixer.make_drink(drink, recipe):
        return "ok\n"
    else:
        raise ServiceUnavailable("Error: %s (%d)" % (mixer.get_error(), ret))


def getRecipeFromDrink(id, drink_size):
	
    drink = db.session.query(Drink) \
                          .filter(Drink.id == id) \
                          .first() 

    boozes = db.session.query(Booze) \
                          .join(DrinkBooze.booze) \
                          .filter(DrinkBooze.drink_id == drink.id)
    
    drink.process_ingredients()
    print "Los ingredients: ",drink.ingredients
    content = []
    for ing in drink.ingredients:
    	print ing
    	info = {
    		"name":  ing['name'],
    		"id":    ing['id'],
    		"parts": ing['parts'],
    		"volume"  : 0
    	}
    	content.append(info)
    
    print "El content es: ", content
    total = 0
    for ing in content:
    	total = total + ing['parts']
    
    print "El total de partes es: ", total
    
    recipe = {}
    for ing in content:
    	ing['volume'] = round( (float(drink_size) * float(ing['parts']) ) / float(total))
#     	print "El volumen: ", ing['volume']
    	tag = "booze" + str(ing['id'])
#     	print tag
    	recipe[tag] = ing['volume']
#     	print recipe
    print "La receta calculada es:", recipe
    return recipe



#     for ing in content:
# #     	ing['volume'] = round( (float(drink_size) * float(ing['parts']) ) / float(total))
# #     	print "El volumen es: ", ing['volume']
#     	tag = "booze" + str(ing['id'])
#     	print tag
#     	recipe[tag] = ing['volume']
# 	
# 	print recipe
# 	return recipe
		



# for(i = 0; i < ing.length; i++)
#         {
#             if (i == 0)
#                 args = "?";
#             else 
#                 args += "&";
#             args += "booze" + ing[i].id + "=";
#             volume = is_taster ? ing[i].taster_volume.toFixed(0) : ing[i].volume.toFixed(0);
#             args += volume;
#         }
	
#  var drink_size = {{ options.drink_size }};    
#     var ing = [ 
#    {% for ing in drink.ingredients %}
#       { 
#         'name'           : '{{ ing.name }}', 
#         'id'             : {{ ing.id }}, 
#         'parts'          : {{ ing.parts}}, 
#         'newparts'       : 0,
#         'volume'         : 0,
#         'taster_volume'  : 0,
#         'type'           : {{ ing.type }}
#       },
#    {% endfor %}
# ];

#     for(i = 0; i < ing.length; i++)
#     {
#         ing[i].newparts = ing[i].parts;
#         total += ing[i].newparts;
#     }

#     for(i = 0; i < ing.length; i++)
#     {
#         ing[i].volume = drink_size * ing[i].newparts / total;
#         
#     } 



# def update_volumes():
# 
#     total = 0;
#     for(i = 0; i < ing.length; i++)
#     {
#         if (ing[i].type == 1) // Alcohol
#             ing[i].newparts = ing[i].parts + (ing[i].parts * .25 * drink_strength);
#         else
#         if (ing[i].type == 2) // tart
#             ing[i].newparts = ing[i].parts + (ing[i].parts * .25 * drink_tartness);
#         else
#         if (ing[i].type == 3) // sweet
#             ing[i].newparts = ing[i].parts + (ing[i].parts * .25 * -drink_tartness);
#         else
#             ing[i].newparts = ing[i].parts;
# 
#         total += ing[i].newparts;
#     } 
#     for(i = 0; i < ing.length; i++)
#     {
#         ing[i].volume = drink_size * ing[i].newparts / total;
#         ing[i].taster_volume = taster_size * ing[i].newparts / total;
#         
#     } 



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
  

    allDrinks = []
    allDrinks.append(['topDrinks', topDrinks])
    allDrinks.append(['otherDrinks', otherDrinks])    

    
    return jsonify(AllDrinks=[{'topDrinks':topDrinks}, {'otherDrinks':otherDrinks}])    


@app.route('/ws/drink_info/<id>')
def drink_info(id):
    drink = db.session.query(Drink) \
                          .filter(Drink.id == id) \
                          .first() 

    boozes = db.session.query(Booze) \
                          .join(DrinkBooze.booze) \
                          .filter(DrinkBooze.drink_id == drink.id)

    drink.process_ingredients()

    has_non_alcohol = False
    has_alcohol = False
    has_sweet = False
    has_tart = False
    show_sobriety = 0 #drink.id == 46
    for booze in boozes:
        if booze.type == BOOZE_TYPE_ALCOHOL: 
            has_alcohol = True
        else:
            has_non_alcohol = True
        if booze.type == BOOZE_TYPE_SWEET: has_sweet = True
        if booze.type == BOOZE_TYPE_TART: has_tart = True

    show_sweet_tart = has_sweet and has_tart
    show_strength = has_alcohol and has_non_alcohol
    
    jsonDrink = []
    jsonDrink.append({ 'id'  : drink.id,
                       'desc': drink.desc.encode('utf8'), 
                       'name_id' : drink.name_id,
                       'sugg_size' : drink.sugg_size,
                       'ingredients' : drink.ingredients
                     })
                     
    return jsonify(	drink=jsonDrink, 
#     				options=app.options,
    				title=drink.name.name.encode('utf8'),
    				is_custom=0,
    				show_sweet_tart=show_sweet_tart,
    				show_sobriety=show_sobriety,
    				can_change_strength=show_strength
    			)

               
    
    
    
    