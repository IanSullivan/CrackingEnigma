import string
import random


class Rotor:
    def __init__(self, wiring, turnover):
        self.wiring = wiring
        self.turnover = turnover
        self.position = 0

    def forward(self, c):
        idx = (string.ascii_uppercase.index(c) + self.position) % 26
        return self.wiring[idx]

    def backward(self, c):
        idx = (self.wiring.index(c) - self.position) % 26
        return string.ascii_uppercase[idx]

    def rotate(self):
        self.position = (self.position + 1) % 26

    def at_turnover(self):
        return self.position == self.turnover


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, c):
        idx = string.ascii_uppercase.index(c)
        return self.wiring[idx]


class Plugboard:
    def __init__(self):
        self.mapping = {}

    def add_pair(self, c1, c2):
        if c1 not in self.mapping and c2 not in self.mapping:
            self.mapping[c1] = c2
            self.mapping[c2] = c1

    def process(self, c):
        if c in self.mapping:
            return self.mapping[c]
        else:
            return c


class EnigmaMachine:
    def __init__(self, rotor_wirings, rotor_turnovers, reflector_wiring):
        self.rotors = []
        for wiring, turnover in zip(rotor_wirings, rotor_turnovers):
            rotor = Rotor(wiring, turnover - 1)
            for _ in range(turnover):
                rotor.rotate()
            self.rotors.append(rotor)
        self.reflector = Reflector(reflector_wiring)
        self.plugboard = Plugboard()
        self.wrong_plugs = Plugboard()

    def reset_rotors(self):
        for rotor in self.rotors:
            rotor.position = rotor.turnover + 1 % 26

    def set_plugboard_pairs(self, pairs):
        for pair in pairs:
            self.plugboard.add_pair(pair[0], pair[1])
            self.plugboard.add_pair(pair[1], pair[0])

    def encrypt(self, message):
        message = message.upper()
        encrypted_message = ""
        for c in message:
            if c.isalpha():
                self.rotate_rotors()
                c = self.plugboard.process(c)
                encrypted_char = self.pass_through_rotors(c)
                encrypted_char = self.reflector.reflect(encrypted_char)
                encrypted_char = self.pass_through_rotors_backwards(encrypted_char)
                encrypted_char = self.plugboard.process(encrypted_char)
                encrypted_message += encrypted_char
        return encrypted_message

    def decrypt(self, message, crib):
        message = message.upper()
        for i, c in enumerate(message):
            if c.isalpha():
                self.rotate_rotors()
                if c in self.plugboard.mapping:
                    encrypted_char = self.send_through(c, crib[i])
                elif crib[i] in self.plugboard.mapping:
                    encrypted_char = self.send_through(crib[i], c)
                else:
                    encrypted_char = c
                if not encrypted_char:
                    return False
        return True

    def send_through(self, query_letter, target_letter):
        c = self.plugboard.process(query_letter)
        encrypted_char = self.pass_through_rotors(c)
        encrypted_char = self.reflector.reflect(encrypted_char)
        encrypted_char = self.pass_through_rotors_backwards(encrypted_char)
        if encrypted_char != target_letter:
            # if self.wrong_plugs.process(encrypted_char) == target_letter:
            #     return None
            if encrypted_char in self.plugboard.mapping and encrypted_char != self.plugboard.process(target_letter):
                for k, v in self.plugboard.mapping.items():
                    self.wrong_plugs.add_pair(k, v)
                self.wrong_plugs.add_pair(encrypted_char, target_letter)
                return None
            self.plugboard.add_pair(encrypted_char, target_letter)
        return self.plugboard.process(encrypted_char)

    def rotate_rotors(self):
        self.rotors[0].rotate()
        for i in range(len(self.rotors) - 1):
            if self.rotors[i].at_turnover():
                self.rotors[i + 1].rotate()

    def pass_through_rotors(self, c):
        for rotor in self.rotors:
            c = rotor.forward(c)
        return c

    def pass_through_rotors_backwards(self, c):
        for rotor in reversed(self.rotors):
            c = rotor.backward(c)
        return c


def generate_random_plugboard_pairs(num_pairs):
    alphabet = list(string.ascii_uppercase)
    available_letters = alphabet.copy()
    plugboard_pairs = []

    for _ in range(num_pairs):
        if len(available_letters) < 2:
            break
        letter1 = random.choice(available_letters)
        available_letters.remove(letter1)
        letter2 = random.choice(available_letters)
        available_letters.remove(letter2)
        plugboard_pairs.append((letter1, letter2))

    return plugboard_pairs

# Example usage:
# rotor_wirings = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO"]
# rotor_turnovers = [16, 4, 2]
# reflector_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
#
# enigma = EnigmaMachine(rotor_wirings, rotor_turnovers, reflector_wiring)
# # plugboard_pairs = generate_random_plugboard_pairs(10)
# plugboard_pairs = [('C', 'W'), ('H', 'R'), ('N', 'G'), ('P', 'L'), ('A', 'Y'), ('M', 'J'), ('Q', 'I'), ('O', 'V'), ('F','Z'), ('K', 'D')]
# enigma.set_plugboard(plugboard_pairs)
# message = "WETTERBERICHT"
# encrypted_message = enigma.encrypt(message)
# print("Encrypted message:", encrypted_message)
#
# enigma = EnigmaMachine(rotor_wirings, rotor_turnovers, reflector_wiring)
# enigma.set_plugboard(plugboard_pairs)
# decrypted_message = enigma.encrypt(encrypted_message)
# print("Decrypted message:", decrypted_message)


def main():
    # Enigma settings
    rotor_wirings = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO"]
    rotor_turnovers = [17, 5, 22]
    reflector_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

    # Ciphertext and crib
    ciphertext = "CGLZRABKOQKWZ"
    crib = "WETTERBERICHT"

    # Create the Enigma machine
    enigma = EnigmaMachine(rotor_wirings, rotor_turnovers, reflector_wiring)

    # Make initial plugboard guesses
    plugboard_pairs_guess = [('A', 'Z'), ('B', 'Y'), ('C', 'X'), ('D', 'W'), ('E', 'V')]
    enigma.set_plugboard_pairs(plugboard_pairs_guess)

    # Decrypt the message using the Enigma machine
    decrypted_message = enigma.decrypt(ciphertext, crib)

    # Output the results
    print("Ciphertext:", ciphertext)
    print("Crib:", crib)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()