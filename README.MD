### Welcome to my pyweek entry, named "The Lost Goat".

The game revolves around a ~~goat~~ human named Mr. Goat, who gets lost at sea while having a voyage on his newly bought yacht.
He finds himself on a mysterious island, with a threatening tsunami approaching, and a lot of abandoned computer components.

You need to help him build a computer to contact a rescue team and get out in 15 minutes.<br><br>


### How to run the file
simply create a `venv` using the command `py -m venv venv` on Windows or `python3 -m venv venv` on Mac or Linux
then, do `venv\Scrips\activate` on windows or `source venv\bin\activate` on Mac or Linux
then, install the requirements using `py -m pip install -r requirements.txt` on windows or `python3 -m pip install -r requirements.txt` on mac or linux
To run the python file, you can simply just write `py 'run_game.py'` on Windows, or `'python3 run_game.py'` on Mac or Linux.


#### How to play

You will be welcomed with a start screen with the story and the play and exit button.<br><br>

![Start Screen](https://i.ibb.co/nzwJ1Z4/image.png)<br><br>

If you click on the **Exit** button, you will, ahem, exit.<br>

If you click on **Start**, you will be redirected to a map with all the components scattered on it.<br><br>

![Map](https://i.ibb.co/vdpL9cX/image.png)<br>
Note: The path drawn on the map is just indicative to show most of the components required for building a PC, and should not necessarily be followed in the same order


As you can see, there are multiple red dots on the map, each indicating a computer component that you *can* collect after answering 3 related questions correctly.<br>

You can also see the timer, ticking at the bottom, set for exactly 15 minutes, after which the Tsunami will wash you over!<br><br>

![Clicked on dot on map](https://i.ibb.co/N3NdTHW/image.png)<br>

If you click on a dot, you can see a button pop up, saying which component the dot represents.


Once you click on the button, you can see a different screen with three doors, each of which you need to open to get the component.

![Clicked on button](https://i.ibb.co/94QWD5z/image.png)<br>

If you click on a door, you are presented with a question, and a cursor underneath that, which is where you will need to type to answer the question.<br>

![Clicked on door](https://i.ibb.co/KbZq6mx/image.png)

If you answer it correctly, you can see a green check mark (✔) on the door:

![Green checkmark](https://i.ibb.co/BnjvbG7/image.png)

Otherwise you will hear an error beep. To exit the doors, you can either:  
* Press alt + f4 <br>
* Click on the ❌ (cross)<br>
* Press `esc` <br>

You can come back and answer the incomplete / incorrect answer as many times as you want though out the game.

You can also use these commands to pause the game. (You can only pause the game if you are on the map screen). If you pause the game, you will go back to the start screen (the *Resume* button will replace the *Start* button in this case):
![Pause Screen](https://i.ibb.co/7S22nN2/image.png)

Once all the doors for a component have been ticked, ![Ticked Doors](https://i.ibb.co/H2HfBh5/image.png)you can exit out of the door screen and see that now instead of the dot that there was, there is an image of the component. You can also see the status bar on top update. This means that you have unlocked the component :
![Unlocked Calculator](https://i.ibb.co/sQv9MY8/image.png)

Like this, to finish the game, you need to unlock all the **necessary** components (Note: not all components are necessary to finish), and once you think you have all the components, you need to click on the green dot on the *Communication Hut* to build your PC and establish contact. If you do not have all the components, a message will be printed onto the console saying *"You do not have all the necessary components"*. If you have all the necessary components, you will be met with a success screen:
![Success screen](https://i.ibb.co/BZSsgNS/image.png)
Otherwise you will be met with a failiure screen 😢:
![Failiure screen](https://i.ibb.co/LQxGwnB/image.png)


## Now you can play the game on your own (and ~~google~~ learn about PC components!)