################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys
import random

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
#         color="#"
#         a=os.urandom(3).hex()
#         colora= color + a
#         #print(a)
#         self._hex=a
        super().__init__(window) #, bg=colora)
        # make the GUI fullscreen
        window.after(100, window.attributes, "-fullscreen", "True")
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        self._color = rgbs[0]
        # setup the initial "boot" GUI
        self.setupBoot()
#         return a

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        color = "#" + self._color
        self.config(background=color)
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        
        self._dispcolor = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text=f"Color={self._color}")
        self._dispcolor.grid(row=6, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        
        
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        self._dispcolor.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)
        
        explosion_sound.play()
        time.sleep(5)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # play the explosion sound
        
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

class NumericPhase(PhaseThread):
    def __init__(self, name, component=None, target=None, display_length=0):
        super().__init__(name, component, target)
        # the default value is the current state of the component
        self._value = self._get_int_state()
        # we need to know the previous state to detect state change
        self._prev_value = self._value
        # we need to know the display length (character width) of the pin states (for the GUI)
        self._display_length = display_length
        if wire_num==0:
            self._target="00101"
        if wire_num==1:
            self._target="10001"
        if wire_num==2:
            self._target="10100"


    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # get the component value
            self._value = self._get_int_state()
            # the component value is correct -> phase defused
            if (self._value == self._target):
                self._defused = True
            # the component state has changed
            elif (self._value != self._prev_value):
                # one or more component states are incorrect -> phase failed (strike)
                if (not self._check_state()):
                    self._failed = True
                # note the updated state
                self._prev_value = self._value
            sleep(0.1)

    # checks the component for an incorrect state (only internally called)
    def _check_state(self):
        # get a list (True/False) of the current, previous, and valid (target) component states
        states = self._get_bool_state()
        prev_states = [ bool(int(c)) for c in bin(self._prev_value)[2:].zfill(self._display_length) ]
        valid_states = [ bool(int(c)) for c in bin(self._target)[2:].zfill(self._display_length) ]
        # go through each component state
        for i in range(len(states)):
            # a component state has changed *and* it is in an invalid state -> phase failed (strike)
            if (states[i] != prev_states[i] and states[i] != valid_states[i]):
                return False
        return True

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                # the combination is correct -> phase defused
                if (self._value == self._target):
                    self._defused = True
                # the combination is incorrect -> phase failed (strike)
                elif (self._value != self._target[0:len(self._value)]):
                    self._failed = True
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        # TODO
        self._running = True
        while (True):
            # get the jumper wire states (0->False, 1->True)
            
            sleep(0.1)
            
        
        self._running = False

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            return "".join([ chr(int(i)+65) if pin.value else "." for i, pin in enumerate(self._component) ])

# the pushbutton phase
class Button(PhaseThread):
    colors = [ "R", "G", "B" ]  # the button's possible colors

    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)

        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        self._running = True
        # initialize and index and counter to help iterate through the RGB colors
        rgb_index = 0
        rgb_counter = 0
        while (self._running):
            # set the LED to the current color
            self._rgb[0].value = False if Button.colors[rgb_index] == "R" else True
            self._rgb[1].value = False if Button.colors[rgb_index] == "G" else True
            self._rgb[2].value = False if Button.colors[rgb_index] == "B" else True
            # get the pushbutton's state
            while (self._component.value == True):
                self._pressed = True
                self._color = Button.colors[rgb_index]
                sleep(0.1)
            if (self._pressed):
                self._pressed = False
                if (self._color == self._target):
                    self._defused = True
                else:
                    self._failed = True
                
            
            
            # increment the RGB counter
            rgb_counter += 1
            # switch to the next RGB color every 1s (10 * 0.1s = 1s)
            if (rgb_counter == 30):
                rgb_index = (rgb_index + 1) % len(Button.colors)
                rgb_counter = 0
            sleep(0.1)
        self._running = False

    def __str__(self):
        return "Pressed" if self._value else "Released"

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)
        self._value = self._get_int_state()
        self._prev_value = self._value
        self._display_length = 4

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # get the component value
            self._value = self._get_int_state()
            # the component value is correct -> phase defused
            if (self._value == self._target):
                self._defused = True
            # the component state has changed
            elif (self._value != self._prev_value):
                # one or more component states are incorrect -> phase failed (strike)
                if (not self._check_state()):
                    self._failed = True
                # note the updated state
                self._prev_value = self._value
            sleep(0.1)

    # checks the component for an incorrect state (only internally called)
    def _check_state(self):
        # get a list (True/False) of the current, previous, and valid (target) component states
        states = self._get_bool_state()
        prev_states = [ bool(int(c)) for c in bin(self._prev_value)[2:].zfill(self._display_length) ]
        valid_states = [ bool(int(c)) for c in bin(self._target)[2:].zfill(self._display_length) ]
        # go through each component state
        for i in range(len(states)):
            # a component state has changed *and* it is in an invalid state -> phase failed (strike)
            if (states[i] != prev_states[i] and states[i] != valid_states[i]):
                return False
        return True

    # returns the state of the component as a list (True/False)
    def _get_bool_state(self):
        return [ pin.value for pin in self._component ]

    # returns the state of the component as an integer
    def _get_int_state(self):
        return int("".join([ str(int(n)) for n in self._get_bool_state() ]), 2)

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            return str(self._get_bool_state())

