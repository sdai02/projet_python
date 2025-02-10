from socket import socket, AF_INET, SOCK_STREAM
import sys
import re

def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        match argument:

            case "-ipp" | "--ip_port":
                target_host = sys.argv[2]
                target_port = int(sys.argv[3])

    client = socket(AF_INET, SOCK_STREAM)

    # Choisir un port local différent du port serveur
    client.bind(("0.0.0.0", 50000))  # Change 50000 si nécessaire

    client.connect((target_host, target_port))  # Connexion au serveur


    class answer:
        def __init__(self, message):
            self.message = message

        def response(self):
            

            client.sendall(self.message.encode('utf-8'))
            check = client.recv(4096)
            check_response = check.decode('utf-8')
            print(check_response)
            return check_response

        def regex(self, response):
            if response is None or response == "":
                return
            # Recevoir les 5 premiers octets de la réponse


            # Utilisation de regex pour obtenir les chiffres
            numbers = r"(\d+)\s*[\+\-\*\/]\s*(\d+)"
            match = re.search(numbers, response)
            if match:
                operation = match.group(0).strip()
                if '+' in operation:
                    result = int(match.group(1)) + int(match.group(2))  
                elif '*' in operation:
                    result = int(match.group(1)) * int(match.group(2))  
                elif '/' in operation:
                    result = int(match.group(1)) / int(match.group(2))
                elif '-' in operation:
                    result = int(match.group(1)) - int(match.group(2))
                
            

            result_message = str(result).encode('utf-8')
            client.sendall(result_message)            
            check = client.recv(4096)
            check_response = check.decode('utf-8')
            print(result)
            print(check_response)
            return check_response
            
            




    teste = answer("Stephane/dai/3SI5")
    teste.response()
    teste = answer("10/02")
    teste.response()
    response = teste.response()
    if response:
        teste.regex(response)
        teste.response()





main()




