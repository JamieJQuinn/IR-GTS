# Custom GTS & Wonder Card Server

This Python script allows the hosting of a HTTP server to which retail Nintendo DS cartridges can connect. It makes use of the PokemonClassic network to get the required certificates. It enables transferring Pokémon to and from retail Nintendo DS cartridges, and sending Wonder Cards. It is compatible with all Generation-IV Pokémon games (Diamond, Pearl, Platinum, HeartGold, SoulSilver).

## Requirements

- Docker (Available from https://www.docker.com/)
- Generation 4 Pokemon game
- Wireless network (WEP or passwordless)
- Administrator priviliges for installing docker

## Installation

1. Clone the repository to your local machine: (or download and extract the `.zip` file)
```bash
git clone https://github.com/DevreeseJorik/IR-GTS-MG.git
```
2. Navigate to the root of the project
```bash
cd /path/to/project/root
```
3. run docker compose
```bash
docker compose up
```

## Setting up the network

Before proceeding, it's important to ensure that your computer/server hosting the script can be accessed from the network the Nintendo DS is connected to. Generation-IV Pokémon games only support connecting to networks with WEP encryption or no password at all. This can be tricky, as modern routers do not all support this insecure protocol.
Additionally, Windows 11 has removed the ability to connect to insecure networks, so both devices can't be on the 
same network. Nevertheless, there are still ways to let the two devices connect.

### Router Configuration:

If possible, configure your router to host a separate network that uses WEP encryption or has no password.
Ensure that both your host machine and the Nintendo DS are connected to the same router. The host machine
does not necessarily need to connect to the unsecure network, as long as it's a network on the same router.

### Using a Hotspot:

If your router doesn't support creating a second subnet or lacks WEP/passwordless options, you can try to use an (old) phone to create a Hotspot. Some modern phones still allow creating insecure Hotspots while on a network too.

1. Connect the phone to the same network your host machine is on.
2. Create a hotspot with WEP encryption or no security/password.
3. Connect the Nintendo DS to this hotspot.

Since the phone is on the same subnet as the host machine, it should be able to route traffic to it.

### Using a Hotspot with data (Linux/Windows 10 and below):

Some modern phones allow creating insecure Hotspots, but not while connected to a network. This can still
be used for the Nintendo DS, but Windows 11 generally won't let you connect to it. If you're using certain
Linux distributions or Windows 10 and below, you could connect both the host machine and ds to the phone.

Just be aware that this will use data.

### Port-forwarding

If you're unable to have your host machine and Nintendo DS on the same network but can connect the DS to an insecure network (such as using a hotspot with data, but the host machine uses Windows 11), you have the option to port-forward the host machine. This allows the public IP of the host machine to be reached from the Nintendo DS.

The exact steps to perform this are highly dependent on the router/provider you have, so this won't be explained here.

# Usage

1. edit the docker-compose.yaml and replace YOUR_HOST_IP_HERE with your computer's IP address
- Linux: ifconfig
- Windows: ipconfig
2. Run docker compose to start the DNS spoofer and HTTP server:
```bash
docker compose up
```
3. Make note of the 'Primary DNS server' ip address provided by the script, as it will be required for the next step.
4. On your Nintendo DS:
- Boot up the game and navigate to `NINTENDO WFC SETTINGS`, then `Nintendo Wi-FI Connection Settings`.
- Create a new connection and connect to the insecure network.
- Set the Primary DNS to the IP address provided by the script. The Secondary should be left blank/the same as the Primary.

**Send a Pokemon to the DS game**

to send a Pokémon file using the GTS (Global Trade Station), follow these steps:

1. go to http://HOST_MACHINE_IP/pokemondpds/worldexchange/select to choose the pkm file you want to send
2. Enter the GTS within the Pokémon game.
3. When prompted, type/copy-and-paste the file path to the PKM file you want to send. For example:
- After a short time, the Pokémon will appear on the DS and be placed in either an empty spot in your party or the first available PC box. This can take a few seconds, as for some reason the connection for this command is rather slow.

Note: Sending more than one Pokémon at a time is not currently possible. You'll need to exit and re-enter the GTS to send another Pokémon.

**Receive a Pokemon from the DS game**

Whenever you `offer` a Pokemon in the GTS, it's data will be received on the host machine automatically. You will receive an error on the DS stating that the Pokemon cannot be offered for trade - this ensures the Pokémon remains in your game. On your host machine it will automatically save the Pokémon under the `Pokemon` directory in the root of the project. It will check if the Pokémon's data has been saved before, to prevent creating duplicates.


## Support

If you encounter an error, please take a screenshot or copy the script output, describe the state of the DS and any associated error codes, and add an issue to Github's issue tracker.


Credits
- LordLandon: Original inspiration and groundwork laid by their SendPKM script.
- ProjectPokemon Community: Extensive documentation on GTS/encryption protocols.
- Infinite Recursion: Initial development of the script.
- Shutterbug: For their development of the nds-constraint exploit, without which this project would be impossible.
- PokeClassic: For the hosting/directing to unofficial servers
that provide the necessary certificates.
- jamiejquinn: Update to function post the shutdown of Nintendo's online services.
- rebrunner: Updating the source code from Python 2 to Python 3.
- RETIREglitch/Jorik Devreese: Complete rewrite of the source code, server architecture and Wonder Card support.
