import itertools
from Enigma import EnigmaMachine
import string

combinations = list(itertools.product(range(1, 27), repeat=3))
alphabet = string.ascii_uppercase
# plug_board_pairs = [('Z', 'T'), ('J', 'R'), ('V', 'A'), ('Y', 'N'), ('Q', 'X'), ('U', 'H'),
# ('B', 'K'), ('G', 'L'), ('M', 'I'), ('W', 'C')]
rotor_wirings = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO"]
rotor_turnovers = [16, 4, 2]
reflector_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
found = 0
possible = 0

message = "EINKFNZXUDRWG"
crib =    "WETTERBERICHT"
found = 0
enigma = EnigmaMachine(rotor_wirings, rotor_turnovers, reflector_wiring)
# for combos in combinations:
#     enigma = EnigmaMachine(rotor_wirings, combos, reflector_wiring)
#     for letter in alphabet:
#         enigma.reset_rotors()
#         enigma.plugboard.mapping.clear()
#         enigma.plugboard.add_pair(letter, "T")
#         encrypted_message = enigma.decrypt(message, crib)
#         if encrypted_message:
#             if combos == (16, 4, 2):
#                 print(combos)
#                 print(enigma.plugboard.mapping)
#                 print("crib")
#
#             found += 1
#             for _letter in alphabet:
#                 if "E" not in enigma.plugboard.mapping:
#                     enigma.plugboard.add_pair(_letter, "E")
#                 enigma.reset_rotors()
#                 encrypted_message = enigma.decrypt(message, crib)
#                 if encrypted_message:
#                     # print(combos)
#                     found += 1
#
# print(found)

plugs = {'Z': 'T', 'T': 'Z', 'Y': 'N', 'N': 'Y', 'B': 'K', 'K': 'B', 'J': 'R', 'R': 'J', 'H': 'U', 'U': 'H', 'W': 'C', 'C': 'W', 'L': 'G', 'G': 'L'}
for k, v in plugs.items():
    enigma.plugboard.add_pair(k, v)
plugsBoard = enigma.plugboard.mapping
for letter in alphabet:
    enigma.reset_rotors()
    enigma.plugboard.mapping.clear()
    for k, v in plugs.items():
        enigma.plugboard.add_pair(k, v)
    enigma.plugboard.add_pair(letter, "E")
    encrypted_message = enigma.decrypt(message, crib)
    if letter == "E":
        print(len(enigma.plugboard.mapping))
        print(encrypted_message)

