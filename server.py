import socket
import os
import shutil

def servidor():
    host = 'localhost'  # Endereço IP do servidor
    porta = 12345  # Porta que o servidor vai escutar

    # Garante que o diretório de arquivos exista
    if not os.path.exists('./arquivos'):
        os.makedirs('./arquivos')

    # Cria o socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, porta))
    s.listen(5)  # Permite até 5 conexões simultâneas

    print(f'Servidor escutando na porta {porta}')

    while True:
        conn, addr = s.accept()  # Aceita uma conexão
        print(f'Conexão estabelecida com {addr}')

        try:
            comando = conn.recv(1024).decode()  # Recebe o comando do cliente

            if comando == "listar":
                arquivos = os.listdir('./arquivos')  # Lista os arquivos no diretório
                conn.send(str(arquivos).encode())  # Envia a lista de arquivos para o cliente

            elif comando.startswith("excluir"):
                nome_do_arquivo = comando.split(' ')[1]
                caminho_arquivo = os.path.join('./arquivos', nome_do_arquivo)

                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)
                    resposta = f'Arquivo excluído: {nome_do_arquivo}'
                else:
                    resposta = f'Arquivo não encontrado: {nome_do_arquivo}'

                conn.send(resposta.encode())

            elif comando.startswith("enviar"):
                nome_do_arquivo = comando.split(' ', 1)[1]
                caminho_destino = os.path.join('./arquivos', nome_do_arquivo)

                conn.send("OK".encode())  # Confirmação para o cliente

                with open(caminho_destino, 'wb') as arquivo:
                    while True:
                        dados = conn.recv(1024)
                        if not dados or dados == b"EOF":
                            break
                        arquivo.write(dados)

                conn.send(f'Arquivo {nome_do_arquivo} recebido com sucesso.'.encode())

            elif comando.startswith("download"):
                nome_do_arquivo = comando.split(' ', 1)[1]
                caminho_arquivo = os.path.join('./arquivos', nome_do_arquivo)

                if not os.path.exists(caminho_arquivo):
                    conn.send("Erro: Arquivo não encontrado.".encode())
                    conn.close()
                    continue

                conn.send("OK".encode())  # Confirmação inicial
                resposta = conn.recv(1024).decode()  # Aguarda resposta do cliente

                if resposta != "Pronto para receber":
                    conn.close()
                    continue

                with open(caminho_arquivo, 'rb') as arquivo:
                    while True:
                        dados = arquivo.read(1024)
                        if not dados:
                            break
                        conn.send(dados)

                conn.send(b"EOF")  # Indica o fim do arquivo

            else:
                conn.send("Comando não reconhecido".encode())

        except Exception as e:
            print(f"Erro durante a conexão: {e}")

        finally:
            conn.close()  # Fecha a conexão

if __name__ == "__main__":
    servidor()
