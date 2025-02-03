# FTPPlus API

A **FTPPlus** é uma API cliente-servidor para gerenciamento de arquivos, permitindo operações como listar, enviar, excluir e baixar arquivos de um servidor. A API implementa boas práticas de segurança, incluindo sanitização de dados, para garantir a integridade e proteção contra vulnerabilidades.

## Comandos Disponíveis

- **listar**: Lista os arquivos disponíveis no servidor.
- **enviar `<arquivo>`**: Envia um arquivo para o servidor.
- **excluir `<arquivo>`**: Exclui um arquivo do servidor.
- **baixar `<arquivo>`**: Faz o download de um arquivo do servidor.

## Exemplo de Uso

1. **Iniciar o Servidor:**
   Antes de executar o cliente, inicie o servidor Python:
   ```bash
   python servidor.py
   
2. Comandos do Cliente: O cliente pode executar os seguintes comandos para interagir com o servidor:
Listar arquivos: Para listar os arquivos disponíveis no servidor, execute o comando:
   ```bash
    python client.py <ip-do-servidor> "listar"
   ```
	Exemplo de resposta:
	```bash
   { "status": "success", "data": ["arquivo1.txt", "arquivo2.pdf"] }
   ```

	Excluir arquivo:
		Para excluir um arquivo do servidor, execute o comando:
	```bash
	python client.py <ip-do-servidor> "excluir arquivo.txt"
	```
	Exemplo de resposta:
	```bash
	{ "status": "success", "message": "arquivo.txt excluído" }
	```
	Enviar arquivo: Para enviar um arquivo para o servidor, execute o comando:
	  ```bash
	python client.py <ip-do-servidor> "enviar arquivo.txt"
   ```
	Exemplo de resposta:
   ```bash
	{ "status": "success", "message": "arquivo.txt enviado com sucesso" }
	```
	Baixar arquivo: Para baixar um arquivo do servidor, execute o comando:
   ```bash
	python client.py <ip-do-servidor> "baixar arquivo.txt"
	```
	Exemplo de resposta:
	  ```bash
	{ "status": "success", "message": "arquivo.txt salvo com sucesso"}
	```

	 ---

## Sanitização de Dados

A **FTPPlus API** adota práticas rigorosas de sanitização de dados para garantir que as entradas dos usuários sejam seguras e evitar vulnerabilidades de segurança, como injeção de comandos e ataques de caminho. As principais medidas incluem:

- **Validação de Arquivos:**
  - Nomes de arquivos são validados para bloquear caracteres especiais ou sequências perigosas, como `../../`, que podem permitir acesso não autorizado a pastas ou arquivos fora do diretório permitido.
  - Apenas arquivos com nomes válidos e dentro das restrições do sistema de arquivos são aceitos.

- **Comandos Reconhecidos:**
  - A API valida os comandos recebidos e assegura que apenas comandos pré-definidos e reconhecidos (como `listar`, `enviar`, `excluir`, `baixar`) sejam processados.
  - Comandos desconhecidos ou malformados são rejeitados, prevenindo tentativas de injeção maliciosa.

- **Mensagens de Erro Claras:**
  - Quando ocorre um erro, a resposta do servidor fornece mensagens claras e específicas, como:
    ```json
    { "status": "error", "message": "Arquivo não encontrado" }
    ```
  - Mensagens de erro são projetadas para evitar vazamento de informações internas ou detalhes que possam ser usados para explorar o sistema.

- **Escapamento de Entrada:**
  - Todos os dados fornecidos pelo cliente (como nomes de arquivos) são devidamente escapados antes de serem processados, evitando que caracteres especiais sejam interpretados de maneira insegura.

Essas práticas são implementadas para proteger tanto o servidor quanto os clientes, mantendo a comunicação segura e protegida contra ataques comuns.

---

## Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Resumo da Licença MIT

A Licença MIT permite que você faça o que desejar com o código, incluindo copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, desde que a permissão seja fornecida de acordo com os termos seguintes:

- O aviso de copyright e a permissão nesta nota devem ser incluídos em todas as cópias ou partes substanciais do Software.
- O Software é fornecido "como está", sem garantia de qualquer tipo, expressa ou implícita, incluindo, mas não se limitando a garantias de comercialização ou adequação a um fim específico.

Esta licença permite que você use o software para qualquer propósito, mas isenta os desenvolvedores de qualquer responsabilidade ou danos decorrentes do uso do código.
