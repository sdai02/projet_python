from socket import socket, AF_INET, SOCK_STREAM

target_host = "148.113.42.34"
target_port = 27153

client = socket(AF_INET, SOCK_STREAM)

# Choisir un port local différent du port serveur
client.bind(("0.0.0.0", 50000))  # Change 50000 si nécessaire

client.connect((target_host, target_port))  # Connexion au serveur
# Recevoir les 5 premiers octets de la réponse
response = client.recv(4096)
exam_response = response.decode('utf-8')
print(exam_response)


class answer:
    def __init__(self, message):
        self.message = message


    def response(self):
        # Envoyer une chaîne de caractères au serveur
        client.sendall(self.message.encode('utf-8'))
        print("Stephane/dai/3SI5")

        check = client.recv(4096)
        check_response = check.decode('utf-8')
        print(check_response)




teste = answer("Stephane/dai/3SI5")
teste.response()

teste = answer("10/02")
teste.response()

calcule = 888 + 813
teste = answer(str(calcule))
teste.response()











# client.sendall(b"10/02")
# print("10/02")

# check_2 = client.recv(4096)
# check_2_response = check_2.decode('utf-8')
# print(check_2_response)

# calcul = 534 - 386
# client.sendall(b calcul)

