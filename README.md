# RPG-with-pygame
A very first try of using pygame making RPG

Discription:
This is a very simple 2D tiledmap RPG game called "Escape the Town". The player will be chased by monsters and the
only weapon for the player is a gun to fight back. Monsters can use magic! Player has three status: health,
sanity, and crazy. If monsters hit the player, health will loss, if monsters' magic hits the player, health won't
reduce, but it is the mind attack, so sanity will lose. If SAN < 50%, player "went crazy", which means
player starts to loss health 2/time.
There are 2 friendly NPC on the map, Amy will give you a car key to escape here, if you talk to her. (ending Escape)
If you talk to Dismal, he/she will give you a magic book and lead you to the boss, you cannot hurt the boss, 
because it is a "The Old Ones", but your magic book can send him to his own world thus save the town. (ending True victory)
The game has three endings: Die, Escape and True victory. 

How to run the game:
You will need to unzip the file into one folder, leave all inside folders the same as you unzip it. 
Run "main.py" will start the game
"setting.py" are all global variables
"sprite.py" has all sprite groups
"tilemap.py" is used to import tile map file

Library list:
install pytmx (read tiledmap file)
install pygame

Shortcuts:
Press "i" to open player status and inventory
Press "Enter" to restart the game
Clike on NPC to talk with them
Press "Space" to shoot
Press arrow keys to walk
Press Esc to quit
Press "h" to debug collision
