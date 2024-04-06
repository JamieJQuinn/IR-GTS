from struct import unpack, pack
from base64 import b64decode
from .util import Util, Gen4CharMap
from .loghandler import LogHandler
import os, datetime

pokemon_logging = LogHandler('pokemon', 'pokemon.log').get_logger()
class PokemonData:  # Singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance


    def initialize(self):
        self.nature = Util.load_json("./data/natures.json")
        self.species = Util.load_json("./data/species.json")
        self.items = Util.load_json("./data/items.json")
        self.abilities = Util.load_json("./data/abilities.json")
        self.moves = Util.load_json("./data/moves.json")
        self.hidden_powers = Util.load_json("./data/hidden_power.json")
        self.charmap = Gen4CharMap()

        self.base_stats = Util.load_json("./data/base_stats.json")
        self.level_curves = Util.load_json("./data/level_curves.json")
        self.nature_modifiers = Util.load_json("./data/nature_modifiers.json")


class Pokemon:
    def __init__(self, data=None, decrypt=False):
        self.data = self.decrypt_pokemon(data) if decrypt else data

    def set_pid(self, pid):
        self.data[0x00] = pid & 0xFF
        self.data[0x01] = (pid >> 8) & 0xFF
        self.data[0x02] = (pid >> 16) & 0xFF
        self.data[0x03] = (pid >> 24) & 0xFF

    def get_pid(self):
        return self.data[0x00] + (self.data[0x01] << 8) + (self.data[0x02] << 16) + (self.data[0x03] << 24)

    def get_nature(self):
        pid = self.get_pid()
        return PokemonData().nature[pid % 25]

    def set_nature(self, nature):
        pid = self.get_pid()
        if isinstance(nature, str):
            nature = list(PokemonData().nature.keys()).index(nature)
        pid = pid - self.get_nature() + nature
        if pid > 0xFFFFFFFF:
            pid = nature
        self.set_pid(pid)

    def get_encryption_bypass(self):
        return self.data[0x04] & 3

    def set_encryption_bypass(self, bypass):
        self.data[0x04] = (self.data[0x04] & 0xFC) | bypass

    def get_bad_egg_flag(self):
        return (self.data[0x04] >> 1) & 1

    def set_bad_egg_flag(self, bad_egg_flag):
        self.data[0x04] = (self.data[0x04] & 0xFD) | (bad_egg_flag << 1)

    def get_checksum(self):
        return self.data[0x06] + (self.data[0x07] << 8)

    def set_checksum(self, checksum):
        self.data[0x06] = checksum & 0xFF
        self.data[0x07] = (checksum >> 8) & 0xFF

    def is_shiny(self):
        pid = self.get_pid()
        trainer_id = self.get_trainer_id()
        secret_id = self.get_trainer_secret_id()

        pid_high = pid >> 16
        pid_low = pid & 0xffff
        id_xor = trainer_id ^ secret_id
        pid_xor = pid_high ^ pid_low
        return (id_xor ^ pid_xor) < 8

    def get_hidden_power(self):
        ivs = self.get_ivs()
        type_ = 0
        power = 0
        for i, iv in enumerate(["hp", "atk", "def", "spe", "spa", "spd"]):
            type_ += (ivs[iv] % 2) * (2 ** i)
            if 2 <= ivs[iv] % 4 <= 3:
                power += 2 ** i
        type_ = (type_ * 15) // 63
        power = (power * 40) // 63 + 30
        return PokemonData().hidden_powers[type_], power

    # Block A: 0x08 - 0x28
    def get_species_id(self):
        return (self.data[0x09] << 8) + self.data[0x08]


    def get_species(self):
        return PokemonData().species[self.get_species_id()]

    def set_species_id(self, species_id):
        self.data[0x08] = species_id & 0xFF
        self.data[0x09] = (species_id >> 8) & 0xFF

    def get_held_item_id(self):
        return self.data[0x0A] + (self.data[0x0B] << 8)

    def get_held_item(self):
        return PokemonData().items[self.get_held_item_id()]

    def set_held_item(self, item_id):
        self.data[0x0A] = item_id & 0xFF
        self.data[0x0B] = (item_id >> 8) & 0xFF

    def get_trainer_id(self):
        return self.data[0x0C] + (self.data[0x0D] << 8)

    def set_trainer_id(self, trainer_id):
        self.data[0x0C] = trainer_id & 0xFF
        self.data[0x0D] = (trainer_id >> 8) & 0xFF

    def get_trainer_secret_id(self):
        return self.data[0x0E] + (self.data[0x0F] << 8)

    def set_trainer_secret_id(self, secret_id):
        self.data[0x0E] = secret_id & 0xFF
        self.data[0x0F] = (secret_id >> 8) & 0xFF

    def get_experience(self):
        return self.data[0x10] + (self.data[0x11] << 8) + (self.data[0x12] << 16) + (self.data[0x13] << 24)

    def set_experience(self, experience):
        self.data[0x10] = experience & 0xFF
        self.data[0x11] = (experience >> 8) & 0xFF
        self.data[0x12] = (experience >> 16) & 0xFF
        self.data[0x13] = (experience >> 24) & 0xFF

    def get_level(self):
        return 100 # TODO: Implement

    def get_friendship(self):
        return self.data[0x14]

    def set_friendship(self, friendship):
        self.data[0x14] = friendship

    def get_ability_id(self):
        return self.data[0x15]

    def get_ability(self):
        return PokemonData().abilities[self.get_ability_id()]

    def set_ability(self, ability):
        self.data[0x15] = ability

    def get_markings(self):
        return self.data[0x16]

    def set_markings(self, markings):
        self.data[0x16] = markings

    def get_language(self):
        return self.data[0x17]

    def set_language(self, language):
        self.data[0x17] = language

    def get_evs(self):
        ev_bytes = self.data[0x18:0x1e]
        evs = {}
        for i,ev in enumerate(["hp", "atk", "def", "spa", "spd", "spe"]):
            evs[ev] = ev_bytes[i]
        evs["total"] = sum(evs.values())
        return evs

    def set_evs(self, evs):
        ev_bytes = [evs.get(ev, None) for ev in ["hp", "atk", "def", "spa", "spd", "spe"]]
        for i, ev in enumerate(ev_bytes):
            if ev is not None:
                self.data[0x18 + i] = ev

    def get_contest_stats(self):
        contest_bytes = self.data[0x1e:0x24]
        contest_stats = {}
        for i,stat in enumerate(["cool", "beauty", "cute", "smart", "tough", "sheen"]):
            contest_stats[stat] = contest_bytes[i]
        return contest_stats

    def set_contest_stats(self, contest_stats):
        contest_bytes = [contest_stats.get(stat, None) for stat in ["cool", "beauty", "cute", "smart", "tough", "sheen"]]
        for i, stat in enumerate(contest_bytes):
            if stat is not None:
                self.data[0x1e + i] = stat

    def get_sinnoh_ribbons1(self):
        return self.data[0x24:0x28]

    def set_sinnoh_ribbons1(self, ribbons):
        self.data[0x24:0x28] = ribbons

    # Block : 0x28 - 0x48
    def get_move_ids(self):
        return self.data[0x28:0x30]

    def get_moves(self):
        moves = self.get_move_ids()
        moves = unpack('<' + 'H' * (len(moves) // 2), moves)
        return [PokemonData().moves[move] for move in moves]

    def set_moves(self, moves):
        if isinstance(moves[0], str):
            move_ids = [PokemonData().moves[move] for move in moves]
        move_ids = pack('<' + 'H' * len(move_ids), *move_ids)
        self.data[0x28:0x30] = move_ids

    def get_move_pps(self):
        return self.data[0x30:0x34]

    def set_move_pps(self, move_pps):
        self.data[0x30:0x34] = move_pps

    def get_move_pp_ups(self):
        return self.data[0x34:0x38]

    def set_move_pp_ups(self, move_pp_ups):
        self.data[0x34:0x38] = move_pp_ups

    def get_ivs(self):
        iv_bytes = self.data[0x38] + (self.data[0x39] << 8) + (self.data[0x3a] << 16) + (self.data[0x3b] << 24)
        ivs = {}
        for i, iv in enumerate(["hp", "atk", "def", "spe", "spa", "spd"]):
            ivs[iv] = (iv_bytes >> (5 * i)) & 0x1F
        return ivs

    def set_ivs(self, ivs):
        is_egg = self.get_is_egg()
        is_nicknamed = self.get_is_nicknamed()

        iv_bytes = is_egg << 30 | is_nicknamed << 31
        for i, iv in enumerate(["hp", "atk", "def", "spe", "spa", "spd"]):
            iv_bytes |= ivs.get(iv, 0) << (5 * i)

    def get_is_egg(self):
        return (self.data[0x3c] >> 6) & 1

    def set_is_egg(self, is_egg):
        self.data[0x3c] = (self.data[0x3c] & 0xBF) | (is_egg << 6)

    def get_is_nicknamed(self):
        return (self.data[0x3c] >> 7) & 1

    def set_is_nicknamed(self, is_nicknamed):
        self.data[0x3c] = (self.data[0x3c] & 0x7F) | (is_nicknamed << 7)

    def get_hoen_ribbons(self):
        return self.data[0x3c:0x40]

    def set_hoen_ribbons(self, ribbons):
        self.data[0x3c:0x40] = ribbons

    def get_fateful_flag(self):
        return self.data[0x40] & 1

    def set_fateful_flag(self, fateful_flag):
        self.data[0x40] = (self.data[0x40] & 0xFE) | fateful_flag

    def get_gender(self):
        is_female = (self.data[0x40] >> 1) & 1
        if is_female:
            return "female"
        is_genderless = (self.data[0x40] >> 2) & 1
        if is_genderless:
            return "genderless"
        return "male"

    def set_gender(self, gender):
        byte = self.data[0x40] & 0xF9
        if gender == "female":
            self.data[0x40] = byte | 2
        elif gender == "genderless":
            self.data[0x40] = byte | 4

    def get_form_id(self):
        return self.data[0x40] >> 3

    def set_form_id(self, form_id):
        self.data[0x40] = (self.data[0x40] & 7) | (form_id << 3)

    def get_shiny_leaves(self):
        byte = self.data[0x41]
        leafs = []
        for leaf in ["A", "B", "C", "D", "E", "crown"]:
            leafs.append((byte >> leaf) & 1)
            byte >>= 1
        return leafs

    def set_shiny_leaves(self, shiny_leaves):
        byte = self.data[0x41] & 0x3F
        for i, leaf in enumerate(shiny_leaves):
            byte |= leaf << i
        self.data[0x41] = byte

    def get_egg_location_plat(self):
        return self.data[0x44] + (self.data[0x45] << 8)

    def set_egg_location_plat(self, egg_location):
        self.data[0x44] = egg_location & 0xFF
        self.data[0x45] = (egg_location >> 8) & 0xFF

    def get_met_location_plat(self):
        return self.data[0x46] + (self.data[0x47] << 8)

    def set_met_location_plat(self, met_location):
        self.data[0x46] = met_location & 0xFF
        self.data[0x47] = (met_location >> 8) & 0xFF

    # Block C: 0x48 - 0x68
    def get_name(self):
        characters = self.data[0x48:0x5e]
        characters = unpack('<' + 'H' * (len(characters) // 2), characters)
        return PokemonData().charmap.encode_characters(characters)

    def set_name(self, name):
        name = PokemonData().charmap.decode_characters(name)
        name = pack('<' + 'H' * len(name), *name)
        self.data[0x48:0x5e] = name

    def get_origin_game(self):
        return self.data[0x5f]

    def set_origin_game(self, origin_game):
        self.data[0x5f] = origin_game

    def get_sinnoh_ribbons2(self):
        return self.data[0x60:0x64]

    def set_sinnoh_ribbons2(self, ribbons):
        self.data[0x60:0x64] = ribbons

    # Block D: 0x68 - 0x88

    def get_trainer_name(self):
        characters = self.data[0x68:0x78]
        characters = unpack('<' + 'H' * (len(characters) // 2), characters)
        return PokemonData().charmap.encode_characters(characters)

    def set_trainer_name(self, trainer_name):
        trainer_name = PokemonData().charmap.decode_characters(trainer_name)
        trainer_name = pack('<' + 'H' * len(trainer_name), *trainer_name)
        self.data[0x68:0x78] = trainer_name

    def get_egg_date(self):
        return self.data[0x78:0x7b]

    def set_egg_date(self, egg_date):
        self.data[0x78:0x7b] = egg_date

    def get_met_date(self):
        return self.data[0x7b:0x7d]

    def set_met_date(self, met_date):
        self.data[0x7b:0x7d] = met_date

    def get_egg_location_dp(self):
        return self.data[0x7e] + (self.data[0x81] << 8)

    def set_egg_location_dp(self, egg_location):
        self.data[0x7e] = egg_location & 0xFF
        self.data[0x7f] = (egg_location >> 8) & 0xFF

    def get_met_location_dp(self):
        return self.data[0x80] + (self.data[0x83] << 8)

    def set_met_location_dp(self, met_location):
        self.data[0x80] = met_location & 0xFF
        self.data[0x81] = (met_location >> 8) & 0xFF

    def get_pokerus(self):
        return self.data[0x82]

    def set_pokerus(self, pokerus):
        self.data[0x82] = pokerus

    def get_poke_ball(self):
        return self.data[0x83]

    def set_poke_ball(self, poke_ball):
        self.data[0x83] = poke_ball

    def get_met_level(self):
        return self.data[0x84] & 0x3F

    def set_met_level(self, met_level):
        self.data[0x84] = (self.data[0x84] & 0xC0) | met_level

    def get_trainer_gender(self):
        is_female = (self.data[0x84] >> 6) & 1
        return "female" if is_female else "male"

    def set_trainer_gender(self, gender):
        byte = self.data[0x84] & 0xBF
        if gender == "female":
            self.data[0x84] = byte | 0x40

    def get_encounter_type(self):
        return self.data[0x85]

    def set_encounter_type(self, encounter_type):
        self.data[0x85] = encounter_type

    def get_poke_ball_hgss(self):
        return self.data[0x86]

    def set_poke_ball_hgss(self, poke_ball):
        self.data[0x86] = poke_ball

    def get_performance(self):
        return self.data[0x87]

    def set_performance(self, performance):
        self.data[0x87] = performance

    def save(self, directory='Pokemon', extension='pkm'):
        if not os.path.exists(directory):
            os.makedirs(directory)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_name = f"{self.get_species_id()}_{self.get_name()}"

        file_exists, file_path = self.file_exists(directory, base_name)
        if file_exists:
            pokemon_logging.warning(f'Pokemon already saved under {file_path}. Skipping save.')
            return
        
        file_name = f"{directory}/{base_name}_{current_time}.{extension}"
        with open(file_name, 'wb') as f:
            f.write(self.data)

        pokemon_logging.info(f'{file_name} saved successfully.')


    def file_exists(self, directory='Pokemon', base_name=None, extension='pkm'):
        for file_name in os.listdir(directory):
            if file_name.startswith(base_name) and file_name.endswith(extension):
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'rb') as f:
                    if f.read() == self.data:
                        return True, file_path
        return False, None


    def dump(self, file_name='statlog.log'):
        ivs = self.get_ivs()
        evs = self.get_evs()
        hp_type, hp_power = self.get_hidden_power()
        dump = f"{self.get_name()}:{'Shiny' if self.is_shiny() else ''}\n    " \
                f"Level {self.get_level()} {self.get_nature()} {self.get_species()} with {self.get_ability()} ({self.get_gender().capitalize()})\n\n    " \
                f"OT: {self.get_trainer_name()}, ID: {self.get_trainer_id()}, Secret ID: {self.get_trainer_secret_id()}\n    " \
                f"Holding: {self.get_held_item()}, Happiness: {self.get_friendship()}\n    " \
                f"Hidden Power: {hp_type}-type (Power {hp_power})\n\n    " \
                f"Moves: {', '.join(self.get_moves())}\n\n    " \
                f"IVs: HP {ivs['hp']}, Atk {ivs['atk']}, Def {ivs['def']}, " \
                f"SpA {ivs['spa']}, SpD {ivs['spd']}, Spe {ivs['spe']}\n    " \
                f"EVs: HP {evs['hp']}, Atk {evs['atk']}, Def {evs['def']}, " \
                f"SpA {evs['spa']}, SpD {evs['spd']}, Spe {evs['spe']}, " \
                f"Total {self.get_evs()['total']}\n\n" \
                f"{'=' * 80}\n\n"

        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(dump)


    def load(self, file):
        if file.endswith('.pkm') or file.endswith('.pk4'):
            with open(file, 'rb') as f:
                self.data = f.read()

            assert len(self.data) == 236 or len(self.data) == 136, 'Invalid filesize.'
            if len(self.data) == 136:
                self.data = self.add_battle_stats(self.data)
            pokemon_logging.info(f'{file} loaded successfully.')
            return self.data
        pokemon_logging.info('Filename must end in .pkm')


    def add_battle_stats(self, pokemon):
        # TODO: Refactor this code
        from .boxtoparty import add_battle_stats
        return add_battle_stats(pokemon)


    def create_encryption_bypass_pokemon(self, decrypted_pokemon):
        decrypted_pokemon = list(unpack("IHH"+"H"*(len(decrypted_pokemon)//2-4), decrypted_pokemon))
        pid = decrypted_pokemon[0]
        shuffled_pokemon = decrypted_pokemon[:3] + self.shuffle_blocks(decrypted_pokemon[3:], pid) + decrypted_pokemon[67:]
        shuffled_pokemon[1] |= 3 # Set the encryption bypass
        return pack("IHH"+"H"*(len(shuffled_pokemon)-3), *shuffled_pokemon)

    def encrypt_pokemon(self, decrypted_pokemon):
        decrypted_pokemon = list(unpack("IHH"+"H"*(len(decrypted_pokemon)//2-4), decrypted_pokemon))
        pid = decrypted_pokemon[0]
        shuffled_pokemon = decrypted_pokemon[:3] + self.shuffle_blocks(decrypted_pokemon[3:], pid) + decrypted_pokemon[67:]
        encrypted_pokemon = self.pokemon_encryption_pass(shuffled_pokemon)
        return pack("IHH"+"H"*(len(encrypted_pokemon)-3), *encrypted_pokemon)


    def decrypt_pokemon(self, encrypted_pokemon):
        encrypted_pokemon = list(unpack("IHH"+"H"*(len(encrypted_pokemon)//2-4), encrypted_pokemon))
        decrypted_pokemon = self.pokemon_encryption_pass(encrypted_pokemon)
        pid = decrypted_pokemon[0]
        unshuffled_pokemon = decrypted_pokemon[:3] + self.unshuffle_blocks(decrypted_pokemon[3:], pid) + decrypted_pokemon[67:]
        return pack("IHH"+"H"*(len(unshuffled_pokemon)-3), *unshuffled_pokemon)


    def pokemon_encryption_pass(self, pokemon):
        pid, checksum = pokemon[0], pokemon[2] & 0xFFFF

        self.encryption_pass(pokemon, checksum, 3, 67)
        if len(pokemon) > 67:
            self.encryption_pass(pokemon, pid, 67, len(pokemon))
        return pokemon


    # The same XOR encryption algorithm is used for both encryption and decryption
    def encryption_pass(self, encrypted_data, seed, min_, max_):
        for i in range(min_, max_):
            seed = (seed * 0x41C64E6D + 0x6073) & 0xFFFFFFFF
            encrypted_data[i] ^= (seed >> 16)


    def shuffle_blocks(self, blocks, pid):
        block_ids = self.determine_shuffle_block_order(pid)
        shuffled_blocks = []
        for i in range(4):
            shuffled_blocks.extend(blocks[block_ids[i]*16:(block_ids[i]+1)*16])
        return shuffled_blocks


    def determine_shuffle_block_order(self, pid):
        block_positions = {
            'a' : [ 0,0,0,0,0,0,  1,1,1,1,1,1,  2,2,2,2,2,2, 3,3,2,3,3,3 ],
            'b' : [ 1,1,2,2,3,3,  0,0,2,2,3,3,  0,0,1,1,3,3, 0,0,1,1,2,2 ],
            'c' : [ 2,3,1,3,1,2,  2,3,0,3,0,2,  1,3,0,3,0,1, 1,2,0,2,0,1 ],
            'd' : [ 3,2,3,1,2,1,  3,2,3,0,2,0,  3,1,3,0,1,0, 2,1,2,0,1,0 ],
        }
        order = ((pid & 0x3E000) >> 13) % 24
        return [block[order] for block in block_positions.values()]


    def unshuffle_blocks(self, blocks, pid):
        block_ids = self.determine_unshuffle_block_order(pid)
        unshuffled_blocks = []
        for i in range(4):
            unshuffled_blocks.extend(blocks[block_ids[i]*16:(block_ids[i]+1)*16])
        return unshuffled_blocks


    def determine_unshuffle_block_order(self, pid):
        block_positions = {
            'a' : [ 0,0,0,0,0,0,  1,1,2,3,2,3,  1,1,2,3,2,3, 1,1,2,3,2,3 ],
            'b' : [ 1,1,2,3,2,3,  0,0,0,0,0,0,  2,3,1,1,3,2, 2,3,1,1,3,2 ],
            'c' : [ 2,3,1,1,3,2,  2,3,1,1,3,2,  0,0,0,0,0,0, 3,2,3,2,1,1 ],
            'd' : [ 3,2,3,2,1,1,  3,2,3,2,1,1,  3,2,3,2,1,1, 0,0,0,0,0,0 ],
        }
        order = ((pid & 0x3E000) >> 13) % 24
        return [block[order] for block in block_positions.values()]


class SCEncodedPokemon(Pokemon):
    def decrypt_pokemon(self, data: bytearray):
        checksum = int.from_bytes(data[:4], byteorder='big') ^ 0x4a3b2c1d
        data = self.decrypt_sce_data(data[4:244], checksum | (checksum << 16))[4:]
        return super().decrypt_pokemon(data)


    def decrypt_sce_data(self, encrypted_data, state):
        decrypted_data = bytearray()
        for byte in encrypted_data:
            state = (state * 0x45 + 0x1111) & 0x7fffffff
            keybyte = (state >> 16) & 0xff
            decrypted_data.append((byte ^ keybyte) & 0xff)
        return decrypted_data


class B64EncodedPokemon(SCEncodedPokemon):
    def decrypt_pokemon(self, data):
        return super().decrypt_pokemon(b64decode(data.replace('-', '+').replace('_', '/')))