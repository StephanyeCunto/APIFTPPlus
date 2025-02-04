import socket
import os

def criar_diretorio():
    if not os.path.exists('./arquivos'):
        os.makedirs('./arquivos')

def listar_arquivos():
    return str(os.listdir('./arquivos')).encode()

def excluir_arquivo(comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        caminho_arquivo = os.path.join('./arquivos', nome_do_arquivo)
        
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            return f'Arquivo excluído: {nome_do_arquivo}'.encode()
        else:
            return f'Arquivo não encontrado: {nome_do_arquivo}'.encode()
    except IndexError:
        return b'Erro: Nome do arquivo nao especificado'

def receber_arquivo(conn, comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        caminho_destino = os.path.join('./arquivos', nome_do_arquivo)
        
        conn.send(b'OK')
        
        with open(caminho_destino, 'wb') as arquivo:
            while True:
                dados = conn.recv(1024)
                if not dados or dados == b"EOF":
                    break
                arquivo.write(dados)
        
        return f'Arquivo {nome_do_arquivo} recebido com sucesso.'.encode()
    except IndexError:
        return b'Erro: Nome do arquivo nao especificado'

def enviar_arquivo(conn, comando):
    try:
        nome_do_arquivo = comando.split(' ', 1)[1]
        caminho_arquivo = os.path.join('./arquivos', nome_do_arquivo)
        
        if not os.path.exists(caminho_arquivo):
            return 'Erro: Arquivo não encontrado.'.encode()
        
        conn.send(b'OK')
        resposta = conn.recv(1024).decode()
        
        if resposta != "Pronto para receber":
            return b'Erro na transferencia'
        
        with open(caminho_arquivo, 'rb') as arquivo:
            while chunk := arquivo.read(1024):
                conn.send(chunk)
        
        conn.send(b"EOF")
        return None  # Indica que o envio foi concluído
    except IndexError:
        return b'Erro: Nome do arquivo nao especificado'

def processar_comando(conn, comando):
    match comando.split()[0]:
        case "listar":
            return listar_arquivos()
        case "excluir":
            return excluir_arquivo(comando)
        case "enviar":
            return receber_arquivo(conn, comando)
        case "download":
            return enviar_arquivo(conn, comando)
        case _:
            return 'Comando não reconhecido'.encode('utf-8')

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
