# -*- coding: utf-8 -*-
from time import sleep, time
from threading import Thread
from flask import Flask, current_app
from flask.ext.sqlalchemy import SQLAlchemy
import memcache
import thread
from sqlalchemy.orm import mapper, relationship, backref
from bartendro import db, app
from bartendro.model.drink import Drink
from bartendro.model.dispenser import Dispenser
from bartendro.model import drink_booze
from bartendro.model import booze
from bartendro.model import drink_log

TICKS_PER_ML = 2.78
CALIBRATE_ML = 60 
CALIBRATION_TICKS = TICKS_PER_ML * CALIBRATE_ML

LIQUID_OUT_THRESHOLD       = 75
LIQUID_WARNING_THRESHOLD   = 120 

DISPENSER_OUT     = 1
DISPENSER_OK      = 0
DISPENSER_WARNING = 2

CLEAN_CYCLE_MAX_PUMPS = 4   # The maximum number of pumps to run at any one time
CLEAN_CYCLE_DURATION  = 30  # in seconds for each pump

class Mixer(object):
    '''This is where the magic happens!'''

    class MixerState:
        INIT = object()            # the bot is initializing
        READY = object()           # the bot is ready to make drinks
        WARNING = object()         # one or more bottles of booze is low
        OUT_OF_BOOZE = object()    # one of more bottles of booze is OUT
        # not in use yet
        # BUSTED = object()          # out of all booze, can't make ANY drinks

    def __init__(self, driver, mc):
        self.driver = driver
        self.mc = mc
        self.err = ""
        self.disp_count = self.driver.count()
        self.state = Mixer.MixerState.INIT
        self.check_liquid_levels()

    def get_error(self):
        return self.err

    def led_idle(self):
        self.driver.led_idle()

    def led_dispense(self):
        self.driver.led_dispense()

    def led_complete(self):
        self.driver.led_complete()

    def led_clean(self):
        self.driver.led_clean()

    def can_make_drink(self, boozes, booze_dict):
        ok = True
        for booze in boozes:
            try:
                foo = booze_dict[booze]
            except KeyError:
                ok = False
        return ok

    def check_liquid_levels(self):
        if not app.options.use_liquid_out_sensors: 
            self.driver.set_status_color(0, 1, 0)
            state = Mixer.MixerState.READY
            return

        new_state = Mixer.MixerState.READY

        # step 1: ask the dispensers to update their liquid levels
        self.driver.update_liquid_levels()

        # wait for the dispensers to determine the levels
        sleep(.01)

        # Now ask each dispenser for the actual level
        dispensers = db.session.query(Dispenser).order_by(Dispenser.id).all()
        for i, dispenser in enumerate(dispensers):
            if i >= self.disp_count: break

            dispenser.out = DISPENSER_OK
            level = self.driver.get_liquid_level(i)
            if level <= LIQUID_WARNING_THRESHOLD:
                if new_state == Mixer.MixerState.READY:
                    new_state = Mixer.MixerState.WARNING
                if dispenser.out != DISPENSER_WARNING:
                    dispenser.out = DISPENSER_WARNING

            if level <= LIQUID_OUT_THRESHOLD:
                if new_state == Mixer.MixerState.READY or new_state == Mixer.MixerState.WARNING:
                    new_state = Mixer.MixerState.OUT_OF_BOOZE
                if dispenser.out != DISPENSER_OUT:
                    dispenser.out = DISPENSER_OUT

        db.session.commit()

        if new_state == Mixer.MixerState.OUT_OF_BOOZE:
            self.driver.set_status_color(1, 0, 0)
        elif new_state == Mixer.MixerState.WARNING:
            self.driver.set_status_color(1, 1, 0)
        else:
            self.driver.set_status_color(0, 1, 0)

        self.state = new_state
        print "Checking levels done"

        return new_state

    def liquid_level_test(self, dispenser, threshold):
        if not app.options.use_liquid_out_sensors: return

        print "Start liquid level test: (disp %s thres: %d)" % (dispenser, threshold)

        self.driver.update_liquid_levels()
        sleep(.01)

        level = self.driver.get_liquid_level(dispenser)
	print "initial reading: %d" % level
        if level <= threshold:
	    print "liquid is out before starting: %d" % level
	    return

        last = -1
        self.driver.start(dispenser)
        while level > threshold:
            self.driver.update_liquid_levels()
            sleep(.01)
            level = self.driver.get_liquid_level(dispenser)
            if level != last:
                 print "  %d" % level
            last = level

        self.driver.stop(dispenser)
        print "Stopped at level: %d" % level
        sleep(.1);
        level = self.driver.get_liquid_level(dispenser)
        print "motor stopped at level: %d" % level

    def get_available_drink_list(self):
        can_make = self.mc.get("available_drink_list")
        if can_make: 
            return can_make

        add_boozes = db.session.query("abstract_booze_id") \
                            .from_statement("""SELECT bg.abstract_booze_id 
                                                 FROM booze_group bg 
                                                WHERE id 
                                                   IN (SELECT distinct(bgb.booze_group_id) 
                                                         FROM booze_group_booze bgb, dispenser 
                                                        WHERE bgb.booze_id = dispenser.booze_id)""")

        if app.options.use_liquid_out_sensors: 
            sql = "SELECT booze_id FROM dispenser WHERE out == 0 ORDER BY id LIMIT :d"
        else:
            sql = "SELECT booze_id FROM dispenser ORDER BY id LIMIT :d"

        boozes = db.session.query("booze_id") \
                        .from_statement(sql) \
                        .params(d=self.disp_count).all()
        boozes.extend(add_boozes)

        booze_dict = {}
        for booze_id in boozes:
            booze_dict[booze_id[0]] = 1

        drinks = db.session.query("drink_id", "booze_id") \
                        .from_statement("SELECT d.id AS drink_id, db.booze_id AS booze_id FROM drink d, drink_booze db WHERE db.drink_id = d.id ORDER BY d.id, db.booze_id") \
                        .all()
        last_drink = -1
        boozes = []
        can_make = []
        for drink_id, booze_id in drinks:
            if last_drink < 0: last_drink = drink_id
            if drink_id != last_drink:
                if self.can_make_drink(boozes, booze_dict): 
                    can_make.append(last_drink)
                boozes = []
            boozes.append(booze_id)
            last_drink = drink_id

        if self.can_make_drink(boozes, booze_dict): 
            can_make.append(last_drink)

        self.mc.set("available_drink_list", can_make)
        return can_make

    def make_drink(self, id, recipe_arg):

        drink = Drink.query.filter_by(id=int(id)).first()
        dispensers = Dispenser.query.order_by(Dispenser.id).all()

        recipe = []
        size = 0
        for booze in recipe_arg:
            r = None
            booze_id = int(booze[5:])
            for i in xrange(self.disp_count):
                disp = dispensers[i]
                if booze_id == disp.booze_id:
                    r = {}
                    r['dispenser'] = disp.id
                    r['dispenser_actual'] = disp.actual
                    r['booze'] = booze_id
                    r['ml'] = recipe_arg[booze]
                    size += r['ml']
                    break
            if not r:
                self.err = "Cannot make drink. I don't have the required booze: %d" % booze_id
                error(self.err)
                return False
            recipe.append(r)
        
        app.log.info("Making drink: '%s' size %.2f ml" % (drink.name.name, size))
        self.led_dispense()
        dur = 0
        active_disp = []

        # A little display before dispensing -blocks until done
        self.pre_dispense_dance(recipe)
        
        # Make the indios that will dispense, standup 
        for r in recipe:
             indio = app.indios[r['dispenser'] - 1]
             indio.center()
             indio.pee()
        sleep(1)                        # Make sure all indios are standing and create a little suspense 

         # Now start the actual liquid flowing...
        for r in recipe:
            if r['dispenser_actual'] == 0:
                r['ms'] = int(r['ml'] * TICKS_PER_ML)
            else:
                r['ms'] = int(r['ml'] * TICKS_PER_ML * (CALIBRATE_ML / float(r['dispenser_actual'])))
            self.driver.dispense_ticks(r['dispenser'] - 1, int(r['ms']))
            app.log.info("..dispense %d for %d ticks" % (r['dispenser'] - 1, int(r['ms'])))
            active_disp.append(r['dispenser'])
            sleep(.01)
            if r['ms'] > dur: dur = r['ms']

        # Keep looping until all pumps are done or have a current sense error
        swag_dir = False
        while len(active_disp) > 0:
            swag_dir = not swag_dir
            sleep(.5)
            # TODO: Make others dance in the meantime?
            for disp in active_disp:
                try: 
                    indio = app.indios[disp -1]
                    is_disp, is_cs = self.driver.is_dispensing(disp - 1)
                    if is_cs:
                        app.log.error("Current sense detected on pump %d!" % disp)
                        active_disp.remove(disp)
                        break
                    if is_disp:
                        # Swing side to side
                        if swag_dir:
                            indio.center(20,15)
                        else:
                            indio.center(-20,15)
                    else:
                        print "Pump %d is now done dispensing" % disp 
                        # Shake off the liquid then sit
                        def indio_done(indio):
                            sleep(1)
                            indio.center()
                            indio.dick_shake(5, True)
                            indio.sit();
                        thread.start_new_thread(indio_done,(indio,))
                        active_disp.remove(disp)
                except Exception:
                    print "Failed to read status of pump %d" % disp
                    
        # Make sure all the indios are sitting and centered
        sleep(2)
        for indio in app.indios:
            indio.sit();
            indio.center();
        
        self.led_complete()
        app.log.info("drink complete")

        t = int(time())
        dlog = drink_log.DrinkLog(drink.id, t, size)
        db.session.add(dlog)
        db.session.commit()

        if app.options.use_liquid_out_sensors and not self.check_liquid_levels():
            self.leds_panic()
            return False

        FlashGreenLeds(self).start()
        return True 

    def clean(self):
        CleanCycle(self).start()

    def pre_dispense_dance(self,recipe):
        speed = 0
        offset = 90
        accel = 60
        for idx, indio in enumerate(app.indios):
            indio.center()
            indio.stand(0,speed, accel)
            sleep(.2)
        sleep(2)

        # Get a list of participating
        participatingIdx = []
        for r in recipe:
            participatingIdx.append(r['dispenser'] - 1)
        
        # Sit all the ones that won't participate 
        for idx, indio in reversed(list(enumerate(app.indios))):
             if not idx in participatingIdx:
                indio.center()
                indio.sit(0, speed, accel)
                sleep(.1)
        
# TODO: Must raise indios during clean!
class CleanCycle(Thread):
    def __init__(self, mixer):
        Thread.__init__(self)
        self.mixer = mixer

    def run(self):
        # All Indios must stand for this
        for idx, indio in enumerate(app.indios):
            indio.center()
            indio.pee()
        
        disp_on_times = []
        disp_off_times = []
        for i in xrange(self.mixer.disp_count):
            disp_on_times.append(((i / CLEAN_CYCLE_MAX_PUMPS) * CLEAN_CYCLE_DURATION) + (i % CLEAN_CYCLE_MAX_PUMPS))
            disp_off_times.append(disp_on_times[-1] + CLEAN_CYCLE_DURATION)

        self.mixer.led_clean()
        for t in xrange(disp_off_times[-1] + 1):
            for i, off in enumerate(disp_off_times):
                if t == off: 
                    self.mixer.driver.stop(i)
            for i, on in enumerate(disp_on_times):
                if t == on: 
                    self.mixer.driver.start(i)
            sleep(1)
        self.mixer.led_idle()
        # All Indios may sit now
        for idx, indio in enumerate(app.indios):
            indio.center()
            indio.sit()
        

class FlashGreenLeds(Thread):
    def __init__(self, mixer):
        Thread.__init__(self)
        self.mixer = mixer

    def run(self):
        sleep(5);
        self.mixer.led_idle()
