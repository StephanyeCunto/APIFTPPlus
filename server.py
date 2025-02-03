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
    s.listen(1)  # O servidor vai escutar uma conexão por vez
    
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
                nome_do_arquivo = comando.split(' ')[1]  # O nome do arquivo é a segunda palavra do comando
                caminho_arquivo = os.path.join('./arquivos', nome_do_arquivo)
                
                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)  # Exclui o arquivo
                    resposta = f'Arquivo excluído: {nome_do_arquivo}'
                else:
                    resposta = f'Arquivo não encontrado: {nome_do_arquivo}'
                
                conn.send(resposta.encode())  # Envia a resposta para o cliente

            elif comando.startswith("enviar"):
                # Recebe o caminho completo do arquivo
                caminho_completo = comando.split(' ', 1)[1]
                
                # Verifica se o arquivo existe
                if not os.path.exists(caminho_completo):
                    resposta = f'Arquivo não encontrado: {caminho_completo}'
                    conn.send(resposta.encode())
                    continue

                # Extrai apenas o nome do arquivo
                nome_do_arquivo = os.path.basename(caminho_completo)
                
                # Caminho de destino no servidor
                caminho_destino = os.path.join('./arquivos', nome_do_arquivo)
                
                try:
                    # Copia o arquivo para o diretório do servidor
                    shutil.copy2(caminho_completo, caminho_destino)
                    
                    resposta = f'Arquivo recebido e copiado: {nome_do_arquivo}'
                    conn.send(resposta.encode())
                
                except Exception as e:
                    resposta = f'Erro ao copiar arquivo: {str(e)}'
                    conn.send(resposta.encode())

        except Exception as e:
            print(f"Erro durante a conexão: {e}")
        
        finally:
            conn.close()  # Fecha a conexão

if __name__ == "__main__":
    servidor()