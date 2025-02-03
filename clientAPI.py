import socket
import os
import sys
import json
import re

class ClientAPI:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        
    def _sanitize_filename(self, filename):
        filename = os.path.basename(filename)
        filename = re.sub(r'[^\w\-\.]', '', filename)
        
        filename = filename[:255]
        
        return filename
    
    def _create_connection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            return s
        except ConnectionRefusedError:
            return self._error_response("Não foi possível conectar ao servidor")
        except Exception as e:
            return self._error_response(f"Erro de conexão: {str(e)}")
    
    def _error_response(self, message):
        return json.dumps({
            "status": "error",
            "message": message
        })
    
    def listar(self):
        s = self._create_connection()
        if isinstance(s, str):  
            return s
        
        try:
            s.send("listar".encode())
            resposta = s.recv(1024).decode()
            s.close()
            
            return json.dumps({
                "status": "success",
                "data": resposta.split(',')
            })
        except Exception as e:
            return self._error_response(f"Erro ao listar arquivos: {str(e)}")
    
    def excluir(self, filename):
        filename = self._sanitize_filename(filename)
        
        s = self._create_connection()
        if isinstance(s, str): 
            return s
        
        try:
            comando = f"excluir {filename}"
            s.send(comando.encode())
            resposta = s.recv(1024).decode()
            s.close()
            
            return json.dumps({
                "status": "success",
                "message": f"{filename} excluído"
            })
        except Exception as e:
            return self._error_response(f"Erro ao excluir arquivo: {str(e)}")
    
    def enviar(self, filepath):
        if not os.path.exists(filepath):
            return self._error_response("Arquivo não encontrado")
        
        filename = self._sanitize_filename(os.path.basename(filepath))
        
        s = self._create_connection()
        if isinstance(s, str):  
            return s
        
        try:
            comando = f"enviar {filename}"
            s.send(comando.encode())
            resposta = s.recv(1024).decode()
            if resposta != "OK":
                s.close()
                return self._error_response("Servidor não está pronto para receber")

            with open(filepath, 'rb') as arquivo:
                while True:
                    dados = arquivo.read(1024)
                    if not dados:
                        break
                    s.send(dados)
                s.send(b"EOF")

            resposta = s.recv(1024).decode()
            s.close()
            
            return json.dumps({
                "status": "success", 
                "message": f"{filename} enviado com sucesso"
            })
        except Exception as e:
            return self._error_response(f"Erro ao enviar arquivo: {str(e)}")
    
    def download(self, filename):
        filename = self._sanitize_filename(filename)
        
        s = self._create_connection()
        if isinstance(s, str):  
            return s
        
        try:
            download_dir = './downloads'
            os.makedirs(download_dir, exist_ok=True)
            
            comando = f"download {filename}"
            s.send(comando.encode())
            
            resposta = s.recv(1024).decode()
            if resposta == "Erro: Arquivo não encontrado.":
                s.close()
                return self._error_response("Arquivo não encontrado no servidor")
            
            s.send("Pronto para receber".encode())
            
            caminho_destino = os.path.join(download_dir, filename)
            with open(caminho_destino, 'wb') as arquivo:
                while True:
                    dados = s.recv(1024)
                    if dados == b"EOF":
                        break
                    arquivo.write(dados)
            
            s.close()
            
            return json.dumps({
                "status": "success",
                "message": f"{filename} salvo com sucesso"
            })
        except Exception as e:
            return self._error_response(f"Erro no download: {str(e)}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python client.py <host> <comando> [parametro]")
        print("Comandos: listar, excluir, enviar, download")
        sys.exit(1)
    
    host = sys.argv[1]
    comando = sys.argv[2]
    
    client = ClientAPI(host)
    
    if comando == "listar":
        print(client.listar())
    elif comando == "excluir" and len(sys.argv) == 4:
        print(client.excluir(sys.argv[3]))
    elif comando == "enviar" and len(sys.argv) == 4:
        print(client.enviar(sys.argv[3]))
    elif comando == "download" and len(sys.argv) == 4:
        print(client.download(sys.argv[3]))
    else:
        print("Comando inválido ou número de argumentos incorreto")
        sys.exit(1)

if __name__ == "__main__":
    main()