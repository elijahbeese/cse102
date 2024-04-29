# cse102



Defuse the Bomb | A CSC 102 Project
Team: 8
BOMB DEFUSAL MANUAL
Version 1 




Defuse the Bomb | A CSC 102 Project 
Introduction

The Game:
This project is based on the game Keep Talking and Nobody Explodes, a cooperative bomb defusing party game. As the game designers put it, “You’re alone in a room with a bomb. Your friends, the 'Experts', have the manual needed to defuse it. But there’s a catch: the Experts can’t see the bomb, so everyone will need to talk it out – fast! Put your puzzle-solving and communication skills to the test as you and your friends race to defuse bombs quickly before time runs out!”

Their version is a software game. Our version takes the idea and realizes it as a physical hardware device with buttons, switches, and more! Although our version can be played just like theirs, players can interact with both the bomb and this document at the same time (i.e., players can simultaneously defuse the bomb and serve as the “Experts”, using this document to help disarm the phases).

The backend of our version of the game is a Raspberry Pi computer that combines a typical computer with the ability to interact with the outside world through sensors. The underlying software is written in Python and is the result of a final group-based project in CSC 102 (The Science of Computing II) in the Computer Science Program at the University of Tampa.

Defusing Bombs:
The bomb will “explode” when its countdown reaches 0:00 or when too many strikes have occurred. You defuse the bomb by disarming all of its phases before the countdown expires.

Phases:
The bomb has four phases, each of which must be disarmed to defuse the bomb. The phases can be disarmed in any order. Once a phase is disarmed, it becomes inactive and changing it doesn't affect the bomb. Instructions for disarming the phases are provided in this document.

Strikes:
A mistake in disarming a phase results in a strike. Get too many strikes, and the bomb “explodes”. Sometimes, the remaining countdown time will be decreased and/or tick faster when a certain number of strikes has occurred.

Information:
A random version of the bomb is presented each time it is “booted”. There are 6,720 unique versions of the bomb with a whopping 1,176,000 possible variations!

Disarming some phases will require specific information about the bomb. Pay close attention to the “bootup” text on the bomb's screen.




Defuse the Bomb | A CSC 102 Project
The Toggles

Regarding the Toggles:
It's so tempting to just toggle the switches over and over with those bright red LEDs and cool switch covers that you can flip. But one wrong toggle gets you one step closer to...BOOM!

In the realm of defusing this enigmatic bomb, the toggles phase has undergone a profound transformation. No longer tethered to the mundane digits of the bomb's serial number, we've imbued it with the unpredictable allure of a randomized sequence.

To embark on this phase of the challenge, you must first unlock the secret encoded within the bomb's serial number. Each numeric digit is a piece of the puzzle, waiting to be assembled into a target value. Once you've meticulously summed these digits, a tantalizing target value emerges, a numerical beacon guiding your path.

But fear not, for the journey doesn't end there. With your target value in hand, you must now embark on the sacred rite of binary conversion. Transforming your target into a 4-digit binary code, you wield the power of toggles to manifest this cryptic language of zeroes and ones.

The left-most toggle, a towering sentinel, bears the weight of the Most Significant Bit (MSB), while its comrades stand in silent vigilance, each representing a descending power of two. Together, they form a symphony of illumination, with LEDs flickering to life, painting the darkness with the language of binary.




Defuse the Bomb | A CSC 102 Project
The Button

Regarding the Button:
The button behaves in unpredictable ways. Follow the instructions below closely to avoid a strike!

Amidst the pulsating backdrop of shifting colors, the bomb's button beckons like a beacon of hope amidst the chaos. With each blink, it tantalizingly hints at the path to salvation, cycling through the primary hues of red, green, and blue. Yet, its true significance lies in sync with the background color, where the highest value reigns supreme. The player must discern this subtle interplay of colors, waiting for the precise moment when the button aligns with the dominant hue. 

With bated breath, they await the opportune instant to press down, their actions synchronized with the rhythm of the bomb's digital heartbeat. Each press is a gamble, a calculated risk in the high-stakes game of defusal. Success demands split-second timing and unwavering resolve, as the player strives to outwit the bomb's cunning design and emerge triumphant amidst the swirling sea of colors.




Defuse the Bomb | A CSC 102 Project
The Keypad

Regarding the Keypad:
Ooooh, an encrypted phase! Press the correct keys on the keypad carefully to avoid a strike. Try to avoid calling the “operator”.

In this intriguing phase, the bomb springs to life with a burst of vibrant color as the Raspberry Pi conjures a random hexadecimal value, serving as the backdrop to the GUI. The hues dance across the screen, painting a kaleidoscope of possibilities. As the player gazes upon this ever-changing canvas, they must decipher the secrets hidden within the digits.

With nimble fingers, they punch in the decimal equivalent of the mysterious hexadecimal color using the number pad. Each correct entry reveals a new surprise, as the background transforms into a fresh palette, challenging the player to adapt swiftly. The race against time intensifies with each cycle, urging the player to maintain focus amidst the dazzling array of colors. 

Success in this phase hinges on a delicate balance of precision, speed, and a keen eye for color theory.




Defuse the Bomb | A CSC 102 Project
The Wires

Regarding the Wires:
Which wires should you “cut”? One wrong “snip” leads you one step closer to an “explosion”!

As the player delves deeper into the bomb's intricate design, they encounter a trio of wires poised like silent sentinels, each representing a different primary color: red, blue, and green. Yet, their significance extends beyond mere aesthetics, as they hold the key to unraveling the bomb's enigmatic puzzle.

Observing the background color with analytical scrutiny, the player must discern the dominant hue, decoding its RGB values to determine the wire-cutting sequence. In a test of wits and reflexes, they deftly snip the wires in descending order, carefully navigating the labyrinth of electrical connections.

With each precise cut, the tension mounts, amplifying the sense of urgency as the bomb's countdown ticks ever closer to zero. Only through strategic thinking and swift action can the player navigate this perilous phase, inching closer to victory while evading the specter of failure.







Puzzle Ideas
Puzzle 1: Switches
Binary with relation to ‘serial number’
Puzzle 2: Wires
Cut in descending order based off number values
Puzzle 3: Button	
Press when button represents color of highest value background color
Puzzle 4: Keypad
 Translate hexidecimal from background to decimal

Trying to figure our how to display the background color on the gui

The pi will create a random hexadecimal value that corresponds to the background of the gui. The number pad will be used to input the decimal value of the translated hexadecimal value. A new background color will be picked. There is one red, one blue, and one green wire on the bomb. The player will have to cut each wire in descending order corresponding to the highest value (if the value is (200,145,175), the player would remove red then blue then green). A new random background color will be picked. The button will flash between red green and blue. The player will have to press down on the button when it is on the color that has the highest value in the background color (if the value is (200,145,175), the player will press the button when the number is red). I'm not exactly sure what to do with the switches but I plan to have them act as some sort of representation of binary.


Lcd, Pushbutton, and Bomb classes: 
These are responsible for creating the GUI for different types of bombs - LCD, pushbutton, and a combination of different components respectively. They set up the initial boot GUI and handle the setup and conclusion of the bomb defusal process.
Timer class: 
Manages the countdown timer functionality, running as a separate thread and updating the display accordingly.
Pushbutton class: 
Represents the pushbutton component of the bomb, allowing for pushing the button and changing its LED color.
PhaseThread class: 
Base class for different phases of the bomb. It provides common functionalities like starting and stopping the phase thread.
Wires and Toggles classes: 
Represent the jumper wires and toggle switches phases respectively. They check if the wires are correctly cut or toggle switches are set correctly.
BombPhases class: 
Manages all the phases of the bomb, starting them as separate threads and waiting for their completion.
Keypad class: 
Represents the keypad phase, checking if the entered sequence matches the target sequence.
BombTimer class: 
Represents the bomb timer phase, checking if the time has run out.
Main functions: 
Entry points for running the bomb scenarios based on the selected bomb type specified in the configuration.


Additional Classes and Functionality: 
The second program includes additional classes such as `Timer`, `Pushbutton`, `Bomb`, `BombPhases`, `Keypad`, and `BombTimer`. These classes provide more detailed representations of different components and phases of the bomb, allowing for a more comprehensive simulation.
GUI Setup and Interaction: 
The second program includes more extensive GUI setup and interaction, with separate classes for different types of bombs (`Lcd`, `Pushbutton`, `Bomb`) and their respective components. This allows for a more visually appealing and interactive user experience.
Thread Management: 
The second program utilizes threading more extensively, with separate threads for managing the timer, phases of the bomb, and user interaction. This adds a layer of complexity but also allows for more efficient handling of concurrent tasks.
Configuration Options: 
The second program includes configuration options such as `BOMB_TYPE`, `SHOW_BUTTONS`, and `RPi`, providing more flexibility in customizing the behavior and appearance of the bomb simulation.
Error Handling: 
The second program includes error handling mechanisms, such as handling exceptions when accessing GPIO pins (`RPi`), ensuring a more robust execution environment.

