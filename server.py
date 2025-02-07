import socket
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def criar_diretorio():
    caminho_pasta = os.path.join(BASE_DIR, 'arquivos')  
    if not os.path.exists(caminho_pasta):
        try:
            os.makedirs(caminho_pasta)
            print(f'Diretório criado: {caminho_pasta}')
        except Exception as e:
            print(f'Erro ao criar diretório: {e}')
    else:
        print(f'Diretório já existe: {caminho_pasta}')


def listar_arquivos():
    return str(os.listdir(BASE_DIR,'arquivos')).encode()

def _sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\-\.]', '', filename)
    return filename[:255]  

def excluir_arquivo(comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        nome_do_arquivo = _sanitize_filename(nome_do_arquivo)
        caminho_arquivo = os.path.join(BASE_DIR,'arquivos', nome_do_arquivo)

        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            return f'Arquivo excluído: {nome_do_arquivo}'.encode()
        else:
            return f'Arquivo não encontrado: {nome_do_arquivo}'.encode()
    except IndexError:
        return 'Erro: Nome do arquivo não especificado'

def receber_arquivo(conn, comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        nome_do_arquivo = _sanitize_filename(nome_do_arquivo)
        caminho_destino = os.path.join(BASE_DIR,'arquivos', nome_do_arquivo)

        conn.send(b'OK')

        with open(caminho_destino, 'wb') as arquivo:
            while True:
                dados = conn.recv(1024)
                if not dados or dados == b"EOF":
                    break
                arquivo.write(dados)

        return f'Arquivo {nome_do_arquivo} recebido com sucesso.'.encode()
    except IndexError:
        return 'Erro: Nome do arquivo não especificado'

def enviar_arquivo(conn, comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        nome_do_arquivo = _sanitize_filename(nome_do_arquivo)
        caminho_arquivo = os.path.join(BASE_DIR,'arquivos', nome_do_arquivo)

        if not os.path.exists(caminho_arquivo):
            return 'Erro: Arquivo não encontrado.'

        conn.send(b'OK')
        resposta = conn.recv(1024).decode()

        if resposta.strip() != "Pronto para receber":
            return 'Erro na transferência'

        with open(caminho_arquivo, 'rb') as arquivo:
            while True:
                chunk = arquivo.read(1024)
                if not chunk:
                    break
                conn.send(chunk)

        conn.send(b"EOF")
        return None  # Indica que o envio foi concluído
    except IndexError:
        return 'Erro: Nome do arquivo não especificado'

def processar_comando(conn, comando):
    cmd = comando.split()[0]
    if cmd == "listar":
        return listar_arquivos()
    elif cmd == "excluir":
        return excluir_arquivo(comando)
    elif cmd == "enviar":
        return receber_arquivo(conn, comando)
    elif cmd == "download":
        return enviar_arquivo(conn, comando)
    else:
        return 'Comando não reconhecido'

def servidor():
    criar_diretorio()
    host, porta = 'localhost', 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, porta))
    s.listen(5)

    print(f'Servidor escutando na porta {porta}')

    while True:
        conn, addr = s.accept()
        print(f'Conexão estabelecida com {addr}')

        try:
            comando = conn.recv(1024).decode()
            resposta = processar_comando(conn, comando)
            if resposta:
                conn.send(resposta)
        except Exception as e:
            print(f"Erro durante a conexão: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    servidor()
