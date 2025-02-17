from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import datetime
import base64


class Answer:
    def __init__(self, client):
        self.client = client

    def send_receive(self, message, split_last=False):
        """Envoie un message et retourne la réponse du serveur."""
        self.client.sendall(message.encode('utf-8'))
        check = self.client.recv(4096).decode('utf-8')
        return check.split()[-1] if split_last else check

    def solve_math(self, response):
        """Détecte une opération mathématique, la résout et envoie la réponse."""
        match = re.search(r"(\d+)\s*([\+\-\*])\s*(\d+)", response)
        if match:
            num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
            result = eval(f"{num1} {operator} {num2}")  # Plus rapide
            return self.send_receive(str(result), split_last=True) # premet de recuprer le dernier mots 
        return None

    def decode_base(self, response):
        # decodeur en base 85,32,64
        encodings = {
            base64.b85decode,
            base64.b32decode,
            base64.b64decode,
        }

        for decode in encodings:
            try:
                decoded_message = decode(response.encode()).decode()
                return self.send_receive(str(decoded_message),split_last=True) # ajout de print si besoin
            except Exception:
                continue
        return None  # Aucun décodage réussi

    def morser(self,morse_message):
        morse_dict = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", "--.": "G",
        "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", "--": "M", "-.": "N",
        "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T", "..-": "U",
        "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1",
        "..---": "2", "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8",
        "----.": "9", "/": " "
        }


        decoded_message = ''.join(morse_dict.get(code, '') for code in morse_message.split())
        return decoded_message

    def braille(self, braille_message):
        braille_dict= {
            "⠁": "A", "⠃": "B", "⠉": "C", "⠙": "D", "⠑": "E", "⠋": "F", "⠛": "G", "⠓": "H",
            "⠊": "I", "⠚": "J", "⠅": "K", "⠇": "L", "⠍": "M", "⠝": "N", "⠕": "O", "⠏": "P",
            "⠟": "Q", "⠗": "R", "⠎": "S", "⠞": "T", "⠥": "U", "⠧": "V", "⠺": "W", "⠭": "X",
            "⠽": "Y", "⠵": "Z", 
            " ": " "
        }
        
        new_braille_message = ''.join(braille_dict.get(letter, '?') for letter in braille_message.split())
        return new_braille_message

    def hexa(self, response):

        decoded_bytes = bytes.fromhex(response)

        decoded_message = decoded_bytes.decode('utf-8', errors='ignore')
        if any(c in decoded_message for c in ['.', '-', '/']):
            morse_decoded = self.morser(decoded_message)  # Décodage du morse
        else:
            braille_decoded = self.braille(decoded_message)
            return print(self.send_receive(braille_decoded))

        return self.send_receive(morse_decoded,split_last=True)
    
    def colors(self,response):
        return 0
  

def reader():
    """Lit le compteur depuis un fichier."""
    try:
        with open("counter.txt", "r") as file:
            content = file.read().strip()  # Lire une seule fois
            return int(content) if content.isdigit() else 1000  # Vérifier si c'est un nombre
    except FileNotFoundError:
        return 0



def save(counter):
    """Sauvegarde le compteur dans un fichier."""
    with open("counter.txt", "w") as file:
        file.write(str(counter))


def increment_counter():
    """Incrémente le compteur et le sauvegarde."""
    counter = reader() + 1
    save(counter)
    return counter


def main():
    if len(sys.argv) > 2 and sys.argv[1] in ["-p", "--port"]:
        target_port = int(sys.argv[2])
        local_port = increment_counter()

    client = socket(AF_INET, SOCK_STREAM)
    client.bind(("0.0.0.0", local_port))
    client.connect(("148.113.42.34", target_port))

    # Liste des premières réponses
    responses = [
        "Stephane/dai/3SI5",
        datetime.datetime.now().strftime("%d/%m"),
        "",
        ""
    ]

    answer = Answer(client)

    for message in responses:
        server_response = answer.send_receive(message)

        # Vérification et traitement
        if re.search(r"(\d+)\s*[\+\-\*]\s*(\d+)", server_response):
            calc_response = answer.solve_math(server_response)
            if calc_response:
                decode = answer.decode_base(calc_response)
                if decode:
                    hex = answer.hexa(decode)
                    if hex:
                        answer.hexa(hex)


main()
