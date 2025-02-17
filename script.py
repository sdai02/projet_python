from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import datetime
import base64



class Answer:
    def __init__(self,client ,message):
        self.client = client
        self.message = message


    def response(self):
        # Envoi de message

        self.client.sendall(self.message.encode('utf-8'))
        check = self.client.recv(4096)
        check_response = check.decode('utf-8')
        print(check_response)
        return check_response

    def regex(self, response):
        
        # Regex pour détecter une opération mathématique
        
        
        match = re.search(r"(\d+)\s*([\+\-\*])\s*(\d+)", response)


        if match:
            num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))



            match operator:

                case '+':
                    result = num1 + num2
                case '*':
                    result = num1 * num2
                case '-' :
                    result = num1 - num2

            result_message = str(result).encode('utf-8')
            self.client.sendall(result_message)
            check = self.client.recv(4096).decode('utf-8')
            split_check = check.split(" ")
            target_string = split_check[-1]
            print(check)
            return target_string
        

    


    def base_64(self, response):
        """Essaie plusieurs encodages et envoie la première version valide au serveur immédiatement."""
        
        encodings = {
            base64.b85decode,  # Priorité au plus efficace
            base64.b32decode,
            base64.b64decode,
        }

        for decode in encodings.items():
            try:
                decoded_bytes = decode(response.encode('utf-8'))
                decoded_message = decoded_bytes.decode('utf-8')  # Convertir en string
                
                # Envoi immédiat (on retire le print pour éviter la latence)
                self.client.sendall(decoded_message.encode('utf-8'))
                check = self.client.recv(4096).decode('utf-8')  # Réception immédiate
                print(check)
                return check 

            except Exception:
                continue  # Ignore l'erreur et passe au prochain encodage

        return None  # Aucun décodage ne fonctionne




       
        
  
def reader():
    try:
        with open("counter.txt", "r") as file:
            content = file.read().strip()
            if content.isdigit():
                return int (content)
            else: 
                return 1000
    except FileExistsError:
        return 0

def save(counter):
    with open("counter.txt", "w") as file:
        file.write(str(counter))


def increment_counter(increment_value):
    counter = reader() + 1
    save(counter)
    return counter

def main():


    if len(sys.argv) > 1:
        argument = sys.argv[1]

        match argument:

            case "-p" | "--port":
                target_port = int(sys.argv[2])
                local_port = increment_counter(1000)

    client = socket(AF_INET, SOCK_STREAM)

   
    client.bind(("0.0.0.0", local_port))  
    client.connect(("148.113.42.34", target_port))  


    question_1=[ "Stephane/dai/3SI5",datetime.datetime.now().strftime("%d/%m"),'','']

    for texte in question_1:

        teste = Answer(client, texte)
        server_response = teste.response()



        if re.search(r"(\d+)\s*[\+\-\*]\s*(\d+)", server_response):
            calc_response = teste.regex(server_response)  # Vérifier si la réponse contient un calcul                
            if calc_response:
                teste.response()
                teste.base_64(calc_response)
                teste.response()

                
main()



