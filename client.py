import socket
import sys
import os

def client(ip_do_servidor, comando, caminho_arquivo=None):
    # Cria o socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao servidor na porta 12345
        s.connect((ip_do_servidor, 12345))

        # Lógica de envio de comando diferente para cada tipo de operação
        if comando == "enviar" and caminho_arquivo:
            # Verifica se o arquivo existe
            if not os.path.exists(caminho_arquivo):
                print(f"Erro: Arquivo {caminho_arquivo} não existe.")
                return
            
            # Envia o comando de envio com o caminho completo do arquivo
            s.sendall(f"enviar {caminho_arquivo}".encode())

        else:
            # Para comandos como listar e excluir
            s.sendall(comando.encode())

        # Recebe a resposta do servidor
        resposta = s.recv(1024)
        print('Resposta:', resposta.decode())

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        # Fecha a conexão
        s.close()

def main():
    # Verifica os argumentos de linha de comando
    if len(sys.argv) < 3:
        print("Uso: python cliente.py <ip_do_servidor> <comando> [caminho_do_arquivo]")
        sys.exit(1)

    ip_do_servidor = sys.argv[1]  # O IP do servidor é o primeiro argumento
    comando = sys.argv[2]  # O comando é o segundo argumento
    caminho_arquivo = sys.argv[3] if len(sys.argv) > 3 else None  # O caminho do arquivo é o terceiro argumento, se existir

    client(ip_do_servidor, comando, caminho_arquivo)

if __name__ == "__main__":
    main()