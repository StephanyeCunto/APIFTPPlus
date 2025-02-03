# Importando os módulos necessários
import socket
import sys

# Função para criar o cliente
def client(ip_do_servidor, comando, nome_do_arquivo=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_do_servidor, 12345))  # Conecta ao servidor na porta 12345

    try:
        s.sendall(comando.encode())  # Envia o comando para o servidor

        if comando == "enviar" and nome_do_arquivo:
            with open(nome_do_arquivo, 'rb') as f:
                for data in f:
                    s.sendall(data)

        elif comando == "listar":
            print("Listando arquivos...")

        elif comando.startswith("excluir"):
            print(f"Excluindo o arquivo {nome_do_arquivo}...")

        resposta = s.recv(1024)  # Recebe a resposta do servidor
        print('Resposta:', resposta.decode())
    finally:
        s.close()  # Fecha a conexão

# Função principal para executar o cliente
if __name__ == "__main__":
    ip_do_servidor = sys.argv[1]  # O IP do servidor é o primeiro argumento
    comando = sys.argv[2]  # O comando é o segundo argumento
    nome_do_arquivo = sys.argv[3] if len(sys.argv) > 3 else None  # O nome do arquivo é o terceiro argumento, se existir
    client(ip_do_servidor, comando, nome_do_arquivo)