Infinite Recursion's GTS Script (IR-GTS)

IR-GTS is a Python script that allows you to transfer Pokemon to and from retail Nintendo DS cartridges. It works for all Generation-IV and Generation-V Pokemon games (Diamond, Pearl, Platinum, HeartGold, SoulSilver, Black, and White). Most of the credit goes to LordLandon for his SendPKM script, as well as the rest of the dedicated chaps at ProjectPokemon, without whom this project would be impossible.

IR-GTS should be platform-independent, and has been tested on Windows, Linux and Mac OS X.

Requirements

    Python 2.7 (Available from http://www.python.org)
    DS Pokemon game, and the proper version of IR-GTS for that game
    Wireless network
    Administrator access to your computer

How-To

First, launch the 'ir-gts.py' (ir-gts-bw.py for Black/White) file, either by double-clicking or from a command prompt. This will give you an IP address to use for your DS' DNS Settings (available from the network configuration screen). After you've changed the Primary DNS accordingly, choose an option from the main menu by typing a letter and pressing (Enter):
Send a Pokemon to the DS game (s)

This works in exactly the same way as LordLandon's SendPKM script (in fact, it's almost entirely the same code). When prompted, type in the file path to the PKM file you want to send (e.g. 'C:\Users\InfiniteRecursion\MAWILE.pkm' or, if it's in the Pokemon directory within the ir-gts folder, simply 'Pokemon\MAWILE.pkm'). You should also be able to drag the file into the prompt window, and it will automatically enter the path for you. Press (Enter), and then enter the GTS in-game when prompted. After a short time, the Pokemon will appear on the DS, and be placed in either an empty spot in your party or the first available PC box.

NOTE: IR-GTS-BW cannot send 236-byte Gen-IV .pkm files, and 136-byte Gen-IV files (Boxed Pokemon) will not transfer properly. Most notably, the nickname and OT name usually appears as '????' in these cases. You can convert Gen-IV to Gen-V using either PokeSav or PokeGen.

Sending more than one at a time isn't currently possible, which means that you have to exit and re-enter the GTS to send another.
Receive a Pokemon from the DS game (r)

After choosing this option, IR-GTS will give you a 'Ready to receive from NDS' prompt. Once you see this, enter the GTS and offer the Pokemon you wish to transfer, in the same way as if you were completing an actual GTS trade. After choosing a Pokemon, it doesn't matter what you request; I usually mash (A) through the prompts. You will then receive an error on the DS stating that the Pokemon cannot be offered for trade - this is to prevent accidental deletion if something goes wrong. On your computer, it will automatically try to save the file as (nickname).pkm within the Pokemon directory. If the file already exists, it prompts for a new name.

As of Version 0.30, this will now create (or add to) a statlog.txt file with the stats of the pokemon you send to your computer. Nature, Ability, Shininess, OT ID and Secret ID, IVs, EVs, Level, Attacks, Hidden Power type and base power, Held Item, Gender, and Happiness are all recorded.
Receive multiple Pokemon from the DS game (m)

This works precisely the same way as above, except it won't dump you back to the menu after receiving each one. There is no need to exit and re-enter the GTS for this function. Press (Control) + (C) to return to the main menu.
Support

If the window closes without warning, it's probably encountered an error. Try running the program from a Command Prompt, as it won't close the window that way, and you can then view the full error message. See CommandPrompt for instructions.

NB: I am no longer able to respond to support requests. The program is distributed as-is, and will not change for the foreseeable future.

Enjoy!
-Infinite Recursion
