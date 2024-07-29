import os
import json

class Util:
    @staticmethod
    def load_json(filename):
        with open(filename,"r", encoding="utf8") as f:
            return json.load(f)


class Gen4CharMap(Util):
    def __init__(self):
        self.character_map: dict = self.load_json('./data/char_map.json').get("characters", {})


    def encode_character(self, char_id):
        if char_id == 0xFFFF:
            return None
        return self.character_map.get(format(char_id, '04X'), "")


    def encode_characters(self, char_ids):
        encoded_chars = []
        for char_id in char_ids:
            encoded_char = self.encode_character(char_id)
            if encoded_char is None: break
            encoded_chars.append(encoded_char)
        return ''.join(encoded_chars)


    def decode_character(self, character):
        for id_, encoded_character in self.character_map.items():
            if character == encoded_character:
                return int(id_, 16)
        return 0xFFFF


    def decode_characters(self, characters):
        return [self.decode_character(char) for char in characters]


def get_pkms():
    pkm_files = []
    for item in os.listdir('/Pokemon/'):
        if '.pkm' in item[-4:]:
            pkm_files.append(item)
    if not pkm_files:
        return [None]
    return pkm_files
