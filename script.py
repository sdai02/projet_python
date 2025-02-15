from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import datetime


class Answer:
        def __init__(self,client ,message):
            self.client = client
            self.message = message
        def response(self):


            self.client.sendall(self.message.encode('utf-8'))
            check = self.client.recv(4096)
            check_response = check.decode('utf-8')
            print(check_response)
            return check_response

        def regex(self, response):
            if response is None or response == "" :
                return


            # Ignorer si la réponse est une date au format dd/mm
            if re.match(r"^\d{2}/\d{2}$", response):
                print("Réponse identifiée comme une date. Aucun calcul effectué.")
                return
        
            # Recevoir les 5 premiers octets de la réponse


            # Regex pour détecter une opération mathématique
            pattern = r"(\d+)\s*([\+\-\*])\s*(\d+)"
            match = re.search(pattern, response)

            if match:
                num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
                result = None



                match operator:

                    case '+':
                        result = num1 + num2
                    case '*':
                        result = num1 * num2
                    case '-' :
                        result = num1 - num2

                print(f"Résultat du calcul: {str(result)}")
                result_message = str(result).encode('utf-8')
                self.client.sendall(result_message)
                check = self.client.recv(4096)
                check_response = check.decode('utf-8')
                return check_response


def main():
    if len(sys.argv) > 1:
        argument = sys.argv[1]

        match argument:

            case "-p" | "--port":
                target_host = "148.113.42.34"
                target_port = int(sys.argv[2])

    client = socket(AF_INET, SOCK_STREAM)

    # Choisir un port local différent du port serveur
    client.bind(("0.0.0.0", 50000))  # Change 50000 si nécessaire

    client.connect((target_host, target_port))  # Connexion au serveur


    try:

        responses = [
            "Stephane/dai/3SI5",
            datetime.datetime.now().strftime("%d/%m"),''
        ]

        for message in responses:
            teste = Answer(client, message)
            server_response = teste.response()
            if server_response is None:
                break


        if re.search(r"(\d+)\s*[\+\-\*]\s*(\d+)", server_response):
            calc_response = teste.regex(server_response)  # Vérifier si la réponse contient un calcul                calc_response = teste.regex(server_response)
            if calc_response:
                print("Réponse calculée :", calc_response)
        else:
            print("Réponse non calculée :", server_response)



    except Exception as e:
        print("Erreur de connexion :", e)

    finally:
        client.close()





main()




