#!/usr/bin/env python

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy.orm import mapper, relationship, backref

SQLALCHEMY_DATABASE_URI = 'sqlite:///../bartendro.db'
SECRET_KEY = 'let our bot get you drunk!'
#USERNAME = 'admin'
#PASSWORD = '!freedrinks'
#SERVER_NAME = '10.1.1.138:8080'

app = Flask(__name__,
            static_url_path = "/static",
            static_folder = "../content/static",
            template_folder = "../content/templates")
app.config.from_object(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "/admin/login"
login_manager.setup_app(app)

# Import models
from bartendro.model.drink import Drink
from bartendro.model.custom_drink import CustomDrink
from bartendro.model.drink_name import DrinkName
from bartendro.model.drink_booze import DrinkBooze

from bartendro.model.booze import Booze
from bartendro.model.booze_group import BoozeGroup
from bartendro.model.booze_group_booze import BoozeGroupBooze

from bartendro.model.dispenser import Dispenser
from bartendro.model.drink_log import DrinkLog
from bartendro.model.version import DatabaseVersion

Drink.name = relationship(DrinkName, backref=backref("drink"))

# TODO: This relationship should really be on Drinkbooze
Drink.drink_boozes = relationship(DrinkBooze, backref=backref("drink"))
DrinkBooze.booze = relationship(Booze, backref=backref("drink_booze"))

# This is the proper relationship from above.
#DrinkBooze.drink= relationship(Drink, backref=backref("drink_booze"))

Dispenser.booze = relationship(Booze, backref=backref("dispenser"))
BoozeGroup.abstract_booze = relationship(Booze, backref=backref("booze_group"))
BoozeGroupBooze.booze_group = relationship(BoozeGroup, backref=backref("booze_group_boozes"))
BoozeGroupBooze.booze = relationship(Booze, backref=backref("booze_group_booze"))
CustomDrink.drink = relationship(Drink, backref=backref("custom_drink"))

DrinkLog.drink = relationship(Drink)

# Import views
from bartendro.view import root, trending
from bartendro.view.admin import booze as booze_admin, drink as drink_admin, \
                                 dispenser as admin_dispenser, report, liquidout, user, options
from bartendro.view.drink import drink
from bartendro.view.ws import booze as ws_booze, dispenser as ws_dispenser, drink as ws_drink, \
                              misc as ws_misc, shotbot as ws_shotbot
