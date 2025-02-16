from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import datetime
import base64


class Answer:
    def __init__(self, client):
        self.client = client

    def send_and_receive(self, message):
        """Envoie un message et retourne la réponse du serveur."""
        try:
            self.client.sendall(message.encode('utf-8'))
            return self.client.recv(4096).decode('utf-8')
        except Exception as e:
            print(f"Erreur lors de l'envoi ou de la réception: {e}")
            return ""

    def authenticate(self):
        """Envoie les informations d'authentification."""
        response = self.send_and_receive("Stephane/dai/3SI5")
        return self.send_and_receive(datetime.datetime.now().strftime("%d/%m"))

    def process_response(self, response):
        """Extrait et traite une opération mathématique depuis une réponse."""
        match = re.search(r"(\d+)\s*([\+\-\*])\s*(\d+)", response)
        if match:
            num1, operator, num2 = int(match[1]), match[2], int(match[3])
            # Calcul sans `eval` pour plus de sécurité
            if operator == '+':
                result = num1 + num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '-':
                result = num1 - num2
            print(f"Résultat du calcul: {result}")
            return self.send_and_receive(str(result))
        return response  # Retourne la réponse complète si aucun calcul

    def decode(self, response):
        """Décode un message Base64 si trouvé."""
        match = re.search(r"Question 4: Décoder ce message:\s*([\w+=/]+)", response)
        if match:
            encoded_message = match[1]
            try:
                decoded_message = base64.b64decode(encoded_message).decode('utf-8')
                print(f"Message décodé: {decoded_message}")
                return self.send_and_receive(decoded_message)
            except Exception as e:
                print(f"Erreur lors du décodage: {e}")
        return self.send_and_receive("toto")  # Retourne une réponse par défaut si pas de décodage


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py -p <port>")
        sys.exit(1)

    target_host = "148.113.42.34"
    target_port = int(sys.argv[2])
    local_port = 60000  # Port local que tu souhaites utiliser

    try:
        # Connexion au serveur
        with socket(AF_INET, SOCK_STREAM) as client:
            client.bind(("0.0.0.0", local_port))  # Assure-toi que ce port est libre

            client.connect((target_host, target_port))
            print(f"Connecté au serveur {target_host}:{target_port} avec le port local {local_port}")


class Answer:
    def __init__(self, client):
        self.client = client

    def send_and_receive_all(self, messages):
        """ Envoie plusieurs messages et retourne toutes les réponses du serveur. """
        responses = []
        for message in messages:
            self.client.sendall(message.encode('utf-8'))
            response = self.receive_all(self.client)
            responses.append(response)
        return responses

    def receive_all(self, client, buffer_size=4096):
        """ Réception de tout le message (en cas de réponse longue). """
        data = b""
        while True:
            part = client.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data.decode('utf-8')

    def authenticate(self):
        """ Envoie les informations d'authentification. """
        return "Stephane/dai/3SI5", datetime.datetime.now().strftime("%d/%m")

    def process_response(self, response):
        """ Extrait et traite une opération mathématique depuis une réponse. """
        match = re.search(r"(\d+)\s*([\+\-\*])\s*(\d+)", response)
        if match:
            num1, operator, num2 = int(match[1]), match[2], int(match[3])
            if operator == '+':
                result = num1 + num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '-':
                result = num1 - num2
            print(f"Résultat du calcul: {result}")
            return str(result)
        return response

    def decode(self, response):
        """ Décode un message Base64 si trouvé. """
        match = re.search(r"Question 4: Décoder ce message:\s*([\w+=/]+)", response)
        if match:
            encoded_message = match[1]
            try:
                decoded_message = base64.b64decode(encoded_message).decode('utf-8')
                print(f"Message décodé: {decoded_message}")
                return decoded_message
            except Exception as e:
                print(f"Erreur lors du décodage: {e}")
        return None  # Aucun message décodé trouvé


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py -p <port>")
        sys.exit(1)

    target_host = "148.113.42.34"
    target_port = int(sys.argv[2])
    local_port = 60000

    # Connexion au serveur
    with socket(AF_INET, SOCK_STREAM) as client:
        client.bind(("0.0.0.0", local_port))
        client.connect((target_host, target_port))

        answer = Answer(client)

        # Authentification
        auth_messages = answer.authenticate()
        
        # Préparer toutes les réponses à envoyer
        messages_to_send = [auth_messages[0], auth_messages[1]]  # 1ère et 2ème réponses
        server_responses = answer.send_and_receive_all(messages_to_send)

        # Traiter la 3ème réponse avec un calcul
        processed_response = answer.process_response(server_responses[1])

        # Ajouter la réponse traitée à l'envoi
        messages_to_send.append(processed_response)

        # Recevoir la réponse après le calcul
        server_responses = answer.send_and_receive_all(messages_to_send)

        # Vérifier si la question 4 est présente et la traiter
        final_response = server_responses[-1]  # Dernière réponse
        if "Décoder ce message" in final_response:
            decoded_message = answer.decode(final_response)
            if decoded_message:
                messages_to_send.append(decoded_message)

        # Réenvoyer le message décodé si nécessaire
        server_responses = answer.send_and_receive_all(messages_to_send)

        print(server_responses)  # Afficher toutes les réponses à la fin


if __name__ == "__main__":
    main()

            answer = Answer(client)
            server_response = answer.authenticate()

            final_response = answer.process_response(server_response)

            # Vérifier si la question 4 est présente et la traiter
            if re.search(r"Décoder ce message", final_response):
                final_response = answer.decode(final_response)

            print(final_response)  # Afficher la dernière réponse

    except Exception as e:
        print(f"Erreur de connexion ou d'exécution: {e}")


main()
