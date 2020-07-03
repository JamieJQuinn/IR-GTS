IR-GTS

IR-GTS is a Python script that allows you to transfer Pokemon to and from retail Nintendo DS cartridges. It works for all Generation-IV Pokemon games (Diamond, Pearl, Platinum, HeartGold, SoulSilver). If an Most of the credit goes to LordLandon for his SendPKM script, as well as the rest of the dedicated chaps at ProjectPokemon, without whom this project would be impossible.

The script was originally developed by Infinite Recursion and has been unofficially updated by me, jamiejquinn, to work after the shutdown of Nintendo's online services. Infinite Recursion also developed a version for the Gen-V games Black and White, however I don't own those games and cannot test changes to that script. If anyone would like to work together to test, get in touch.

## Requirements

- Python 2.7 (Available from http://www.python.org)
- DS Pokemon game
- Wireless network (WEP or passwordless)
- Administrator access to your computer

## How-To

First, launch the 'ir-gts.py' file, either by double-clicking or from a command prompt. This will give you an IP address to use for your DS' DNS Settings (available from the network configuration screen). After you've changed the Primary DNS accordingly, choose an option from the main menu by typing a letter and pressing (Enter):

`s`: **Send a Pokemon to the DS game**

This works in exactly the same way as LordLandon's SendPKM script (in fact, it's almost entirely the same code). When prompted, type in the file path to the PKM file you want to send (e.g. 'C:\Users\InfiniteRecursion\MAWILE.pkm' or, if it's in the Pokemon directory within the ir-gts folder, simply 'Pokemon\MAWILE.pkm'). You should also be able to drag the file into the prompt window, and it will automatically enter the path for you. Press (Enter), and then enter the GTS in-game when prompted. After a short time, the Pokemon will appear on the DS, and be placed in either an empty spot in your party or the first available PC box.

Sending more than one at a time isn't currently possible, which means that you have to exit and re-enter the GTS to send another.

`r`: **Receive a Pokemon from the DS game**

After choosing this option, IR-GTS will give you a 'Ready to receive from NDS' prompt. Once you see this, enter the GTS and offer the Pokemon you wish to transfer, in the same way as if you were completing an actual GTS trade. After choosing a Pokemon, it doesn't matter what you request; I usually mash (A) through the prompts. You will then receive an error on the DS stating that the Pokemon cannot be offered for trade - this is to prevent accidental deletion if something goes wrong. On your computer, it will automatically try to save the file as (nickname).pkm within the Pokemon directory. If the file already exists, it prompts for a new name.

`m`: **Receive multiple Pokemon from the DS game**

This works precisely the same way as above, except it won't dump you back to the menu after receiving each one. There is no need to exit and re-enter the GTS for this function. Press (Control) + (C) to return to the main menu.

## Support

If you encounter an error, please take a screenshot or copy the script output, describe the state of the DS and any associated error codes, and add an issue to Github's issue tracker.

Enjoy
- Infinite Recursion (and jamiejquinn)
