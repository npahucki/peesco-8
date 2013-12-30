# -*- coding: utf-8 -*-
from time import sleep
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
                            'name' : drink.name.name,
                            'ingredients' : drink.ingredients
                            })
                            
    otherDrinks = []

    for drink in other_drinks:
        otherDrinks.append({ 'desc' : drink.desc.encode('utf8'),
                            'id' : drink.id, 
                            'name' : drink.name.name,
                            'ingredients' : drink.ingredients
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

#     custom_drink = db.session.query(CustomDrink) \
#                           .filter(drink.id == CustomDrink.drink_id) \
#                           .first()
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

                     
# var ing = [ 
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


#     print drink.ingredients
# 	
#     for ing in drink.ingredients:        
#     	print { 
#         'name'           : ing['name'], 
#         'id'             : ing['id'], 
#         'parts'          : ing['parts'], 
#         'newparts'       : 0,
#         'volume'         : 0,
#         'taster_volume'  : 0,
#         'type'           : ing['type']
#         }

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
# $.ajax({
#                 url: "/ws/drink/" + drink + args,
#                 success: function(html)
#                 {
#                     if (is_taster)
#                         $.modal.close();
#                     else
#                         window.location = "/";
#                 }
#         });




#      if not custom_drink:
#         return render_template("drink/index", 
#                                drink=drink, 
#                                options=app.options,
#                                title=drink.name.name,
#                                is_custom=0,
#                                show_sweet_tart=show_sweet_tart,
#                                show_sobriety=show_sobriety,
#                                can_change_strength=show_strength)
# 
#     dispensers = db.session.query(Dispenser).all()
#     disp_boozes = {}
#     for dispenser in dispensers:
#         disp_boozes[dispenser.booze_id] = 1
# 
#     booze_group = db.session.query(BoozeGroup) \
#                           .join(DrinkBooze, DrinkBooze.booze_id == BoozeGroup.abstract_booze_id) \
#                           .join(BoozeGroupBooze) \
#                           .filter(Drink.id == id) \
#                           .first()
# 
#     filtered = []
#     for bgb in booze_group.booze_group_boozes:
#         try:
#             dummy = disp_boozes[bgb.booze_id]
#             filtered.append(bgb)
#         except KeyError:
#             pass
# 
#     booze_group.booze_group_boozes = sorted(filtered, key=lambda booze: booze.sequence ) 
#     return render_template("drink/index", 
#                            drink=drink, 
#                            options=app.options,
#                            title=drink.name.name,
#                            is_custom=1,
#                            custom_drink=drink.custom_drink[0],
#                            booze_group=booze_group,
#                            show_sweet_tart=show_sweet_tart,
#                            show_sobriety=show_sobriety,
#                            can_change_strength=show_strength)
    
    
    
    
    
    
    