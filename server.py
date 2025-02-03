# Importando os módulos necessários
import socket
import os

# Função para criar o servidor
def servidor():
    host = 'localhost'  # Endereço IP do servidor
    porta = 12345  # Porta que o servidor vai escutar

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, porta))
    s.listen(1)  # O servidor vai escutar uma conexão por vez

    print('Servidor escutando na porta', porta)

    while True:
        conn, addr = s.accept()  # Aceita uma conexão
        print('Conexão estabelecida com', addr)

        comando = conn.recv(1024).decode()  # Recebe o comando do cliente

        if comando == "listar":
            arquivos = os.listdir('.')  # Lista os arquivos no diretório atual
            conn.send(str(arquivos).encode())  # Envia a lista de arquivos para o cliente

        elif comando.startswith("excluir"):
            nome_do_arquivo = comando.split(' ')[1]  # O nome do arquivo é a segunda palavra do comando
            if os.path.exists(nome_do_arquivo):  # Verifica se o arquivo existe
                os.remove(nome_do_arquivo)  # Exclui o arquivo
                resposta = 'Arquivo excluído: ' + nome_do_arquivo
            else:
                resposta = 'Arquivo não encontrado: ' + nome_do_arquivo
            conn.send(resposta.encode())  # Envia a resposta para o cliente

        elif comando.startswith("enviar"):
            nome_do_arquivo = comando.split(' ')[1]  # O nome do arquivo é a segunda palavra do comando
            with open(nome_do_arquivo, 'wb') as f:
                while True:
                    dados = conn.recv(1024)
                    if not dados:
                        break  # Fim do arquivo
                    f.write(dados)  # Escreve os dados no arquivo
            resposta = 'Arquivo recebido: ' + nome_do_arquivo
            conn.send(resposta.encode())  # Envia a resposta para o cliente

        conn.close()  # Fecha a conexão

# Função principal para executar o servidor
if __name__ == "__main__":
    servidor()