import socket
import os

def cliente():
    host = 'localhost'
    porta = 12345

    while True:
        print("\n=== Comandos disponíveis ===")
        print("1. listar -> Lista os arquivos disponíveis")
        print("2. excluir <nome_do_arquivo> -> Exclui um arquivo no servidor")
        print("3. enviar <caminho_do_arquivo> -> Envia um arquivo para o servidor")
        print("4. download <nome_do_arquivo> -> Baixa um arquivo do servidor")
        print("5. sair -> Fecha o cliente")
        
        comando = input("\nDigite o comando: ")
        
        if comando == "sair":
            print("Encerrando conexão...")
            break

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, porta))
        s.send(comando.encode())

        if comando == "listar":
            resposta = s.recv(1024).decode()
            print("Arquivos disponíveis:", resposta)

        elif comando.startswith("excluir"):
            resposta = s.recv(1024).decode()
            print(resposta)

        elif comando.startswith("enviar"):
            caminho_completo = comando.split(' ', 1)[1]

            if not os.path.exists(caminho_completo):
                print("Erro: Arquivo não encontrado.")
                s.close()
                continue

            nome_do_arquivo = os.path.basename(caminho_completo)
            s.send(nome_do_arquivo.encode())

            resposta = s.recv(1024).decode()
            if resposta != "OK":
                print("Erro no servidor.")
                s.close()
                continue

            with open(caminho_completo, 'rb') as arquivo:
                while True:
                    dados = arquivo.read(1024)
                    if not dados:
                        break
                    s.send(dados)

            s.send(b"EOF") 
            print(s.recv(1024).decode())

        elif comando.startswith("download"):
            nome_do_arquivo = comando.split(' ', 1)[1]
            resposta = s.recv(1024).decode()

            if resposta == "Erro: Arquivo não encontrado.":
                print(resposta)
                s.close()
                continue

            s.send("Pronto para receber".encode())

            caminho_destino = os.path.join('./downloads', nome_do_arquivo)
            if not os.path.exists('./downloads'):
                os.makedirs('./downloads')

            with open(caminho_destino, 'wb') as arquivo:
                while True:
                    dados = s.recv(1024)
                    if dados == b"EOF":
                        break
                    arquivo.write(dados)

            print(f"Download concluído: {caminho_destino}")

        else:
            resposta = s.recv(1024).decode()
            print("Resposta do servidor:", resposta)

        s.close()

if __name__ == "__main__":
    cliente()
