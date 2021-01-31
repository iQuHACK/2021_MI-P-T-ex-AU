# Quantum Battleship

## Team: MI(P)T+ex-AU
Sergey Raudik, Anastasia Gracheva, Alexander Morozov, Dmitrii Morozov, Tatiana Bespalova

## Description

This is a new version of a popular game Battleship allowing battleships to have quantum properties.

If a usual battlefield is too deterministic for you and you'd like to let the battleships to be slightly more vivid and unpredictable the solution is to choose the quantum version of the game! 

Being based on an ion-based real quantum computer it allows one to try themself in finding the best strategy to place the ships and to make the shots. Try yourself, but be careful - if have shot and missed, we can't guaranteer that the ship wouldn't be there next time! =)

Your fleet is now quantum and you can place several copies of each ship to the battlefield. Placing the ships remember that the states will entangle and the impossible states will not count. 
For a more interesting gameplay we've also slightly changed the mechanics of shots: you have several shots now and are able to shoose their positions independently. Choose wisely and it will increase your chances to win fast!

Get acquainted to the the world of quantum mechanics and train your quantum intuition. Get in touch with a real quantum computer and feel how your fate is in the "hands" of quantum nature. Have fun and good luck!

## Current version

The current version of the game allows setting a field and then making shots to find (and fix to a certain place all the battleships).
We propose the following strategy of using the current version: one sets the field and then gives it (hidden) to another one who tries to finish the game in a minimal number of turns.

## Future Plans
Multiplayer version is on its way. 
There is still plenty of room to play with amplitudes and complicated entanglement. 


## How to run the game:

Follow the instructions below to launch the game.
`sudo apt-get install python3-tk` or `sudo dnf install python3-tkinter`  
`pipenv install -r 'requirements.txt'`  
`python3 ./main.py`


