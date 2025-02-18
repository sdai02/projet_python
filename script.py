#!/myenv/bin/python


from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import datetime
import base64
import webcolors
from pycipher import Caesar
import nltk
from nltk.corpus import words, stopwords
nltk.download("words")

english_words = set(words.words())


class Answer:
    # Class to handle server responses and perform operations

    def __init__(self, client):
        self.client = client  # Initialize with the client socket

    def send_receive(self, message, split_last=False):
        """Send a message to the server and return the response"""
        self.client.sendall(message.encode("utf-8"))  # Send the message
        check = self.client.recv(4096).decode("utf-8")  # Receive the response
        return (
            check.split()[-1] if split_last else check
        )  # Return the full response or the last word

    def save_answers(self, answers, name):
        """Save answers to a file"""
        with open(f"{name}.txt", "a") as file:
            file.write(answers + "\n")

    def reset_answers_file(self, name):
        """Reset the answers file"""
        with open(f"{name}.txt", "w") as file:
            file.truncate(0)

    def solve_math(self, response):
        """Detect a math operation in the response, solve it, and return the answer"""
        match = re.search(
            r"(\d+)\s*([\+\-\*])\s*(\d+)", response
        )  # Search for a math operation
        if match:
            num1, operator, num2 = (
                int(match.group(1)),
                match.group(2),
                int(match.group(3)),
            )
            result = eval(f"{num1} {operator} {num2}")  # Solve the operation

            self.save_answers(str(result), "answers")  # Save the result in the file

            return self.send_receive(
                str(result), split_last=True
            )  # Return the calculated result
        return None

    def decode_base(self, response):
        """Attempt to decode a message in base85, base32, or base64"""
        encodings = {
            base64.b85decode,
            base64.b32decode,
            base64.b64decode,
        }

        for decode in encodings:
            try:
                decoded_message = decode(
                    response.encode()
                ).decode()  # Decode the message
                self.save_answers(
                    str(decoded_message), "answers"
                )  # Save the decoded message
                return self.send_receive(
                    str(decoded_message), split_last=True
                )  # Return the decoded message
            except Exception:
                continue
        return self.reset_answers_file(
            "answers"
        )  # If decoding fails, reset the answers file

    def morser(self, morse_message):
        """Decode a morse message"""
        morse_dict = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            "-----": "0",
            ".----": "1",
            "..---": "2",
            "...--": "3",
            "....-": "4",
            ".....": "5",
            "-....": "6",
            "--...": "7",
            "---..": "8",
            "----.": "9",
            "/": " ",
        }

        decoded_message = "".join(
            morse_dict.get(code, "") for code in morse_message.split()
        )
        self.save_answers(str(decoded_message), "answers")  # Save the decoded message
        return decoded_message

    def braille(self, braille_message):
        """Decode a braille message"""
        braille_dict = {
            "⠁": "A",
            "⠃": "B",
            "⠉": "C",
            "⠙": "D",
            "⠑": "E",
            "⠋": "F",
            "⠛": "G",
            "⠓": "H",
            "⠊": "I",
            "⠚": "J",
            "⠅": "K",
            "⠇": "L",
            "⠍": "M",
            "⠝": "N",
            "⠕": "O",
            "⠏": "P",
            "⠟": "Q",
            "⠗": "R",
            "⠎": "S",
            "⠞": "T",
            "⠥": "U",
            "⠧": "V",
            "⠺": "W",
            "⠭": "X",
            "⠽": "Y",
            "⠵": "Z",
            " ": " ",
        }

        new_braille_message = "".join(
            braille_dict.get(letter, "") for letter in braille_message.split()
        )
        self.save_answers(
            str(new_braille_message), "answers"
        )  # Save the decoded braille message
        return new_braille_message

    def hexa(self, response):
        """Decode a hexadecimal message"""
        decoded_bytes = bytes.fromhex(response)
        decoded_message = decoded_bytes.decode("utf-8", errors="ignore")
        if any(c in decoded_message for c in [".", "-", "/"]):
            morse_decoded = self.morser(decoded_message)  # Decode morse
        else:
            braille_decoded = self.braille(decoded_message)  # Decode braille
            return self.send_receive(braille_decoded)
        return self.send_receive(morse_decoded, split_last=True)

    def colors(self, response):
        """Decode an RGB color"""
        match = re.search(r"\((\d+),\s*(\d+),\s*(\d+)\)", response)
        if match:
            rgb = match.group(0)
            rgb_parsing = rgb.strip("()").split(",")
            new_rgb = [int(value.strip()) for value in rgb_parsing]
            color_name = webcolors.rgb_to_name(new_rgb)  # Convert RGB to color name
            self.save_answers(str(color_name), "answers")  # Save the color name
            return self.send_receive(color_name, split_last=True)
        return self.reset_answers_file()  # If the color is invalid, reset the file

    def rewind(self, response):
        """Return the line corresponding to the given number"""
        line_number = int(response)
        with open("answers.txt", "r") as file:
            lines = file.readlines()
            if line_number <= len(lines):
                line = lines[line_number - 1].strip()
                self.save_answers(str(line), "answers")  # Save the returned line
                return self.send_receive(line)

    def find(self, response):
        """Search for a specific word in a list"""
        match = re.findall(
            r"[1-7](?=ème)", response
        )  # Search for numbers 1-7 followed by "ème"
        if match:
            self.save_answers(match[0], "caesar")
            new_response = response.split()
            number = int(match[0])
            start_index = new_response.index("liste:") + 1
            real_words = new_response[start_index:]
            letter = real_words[number - 1]
            last_letter = letter[-1]
            return self.send_receive(last_letter)

    def all_answers(self):
        """Retrieve all answers and format them into a single string"""
        with open("answers.txt", "r") as file:
            responses = file.readlines()
        formatted_response = "_".join(
            response.strip() for response in responses
        )  # Format responses

        return self.send_receive(
            formatted_response, split_last=True
        )  # Send the formatted response

    def cesar_code(self, response):
        print(response)
        for shift in range(1, 26):
            decrypted_text = Caesar(key=shift).decipher(response).lower()

            words_in_text = decrypted_text.split()
            if any(word in english_words for word in words_in_text):
                new_response = decrypted_text

                return print(self.send_receive(new_response))
        return None


# Counter management functions
def reader():
    """Read the counter from a file"""
    with open("counter.txt", "r") as file:
        content = file.read().strip()  # Read the content
        return (
            int(content) if content.isdigit() else 10000
        )  # Return 10000 if counter is invalid


def save(counter):
    """Save the counter to a file"""
    with open("counter.txt", "w") as file:
        file.write(str(counter))


def increment_counter():
    """Increment the counter and save it"""
    counter = reader() + 1
    save(counter)
    return counter


# Main function
def main():
    if len(sys.argv) > 2 and sys.argv[1] in ["-p", "--port"]:
        target_port = int(sys.argv[2])  # Target port passed as argument
        local_port = increment_counter()  # Local port

    client = socket(AF_INET, SOCK_STREAM)
    client.bind(("0.0.0.0", local_port))  # Bind to local port
    client.connect(("148.113.42.34", target_port))  # Connect to server

    responses = [
        "Stephane/dai/3SI5",
        datetime.datetime.now().strftime("%d/%m"),
        "",
        "",
    ]  # Initial responses

    answer = Answer(client)

    for message in responses:
        server_response = answer.send_receive(message)

        if message == "Stephane/dai/3SI5":
            answer.save_answers("Stephane/dai/3SI5", "answers")
            answer.save_answers(datetime.datetime.now().strftime("%d/%m"), "answers")

        # Process server responses
        if re.search(r"(\d+)\s*[\+\-\*]\s*(\d+)", server_response):
            calc_response = answer.solve_math(server_response)  # Math processing
            if calc_response:
                decode = answer.decode_base(calc_response)  # Base decoding
                if decode:
                    hex = answer.hexa(decode)  # Hexadecimal decoding
                    if hex:
                        braille = answer.hexa(hex)  # Braille decoding
                        if braille:
                            point = answer.colors(braille)  # Convert to color
                            if point:
                                remember = answer.rewind(point)  # Rewind to get a line
                                if re.search(r"[1-7](?=ème)", remember):
                                    found_it = answer.find(remember)  # Search for the letter
                                    
                                    if found_it :
                                        sumury = answer.all_answers()  # Return all answers
                                        if sumury:
                                            answer.cesar_code(sumury)
                                    else:
                                        print("wrong answers")
                                        answer.reset_answers_file("answer")
                                        return None
                                        
                                else:
                                    print("wrong answers")
                                    answer.reset_answers_file("answers")  # Reset if needed
                                    return None
                else:
                    print("wrong answers")
                    answer.reset_answers_file("answers")  # Reset if decoding fails
                    return None


main()  # Run the program
