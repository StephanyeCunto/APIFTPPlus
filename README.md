# FTP Plus API 📂🌐

## 📚 Trabalho Acadêmico - Redes de Computadores

### 🌐 Visão Geral
O FTP Plus é uma solução de transferência de arquivos desenvolvida em Python como projeto prático para a disciplina de Redes de Computadores, projetada para demonstrar conceitos fundamentais de comunicação cliente-servidor em redes locais.

![Wakatime](https://wakatime.com/badge/user/5a343522-23db-45ae-b20b-54655c392390/project/59187e51-ff5e-49c3-a860-7224598ac2a0.svg)

## 🎯 Objetivo Acadêmico

### Objetivos Principais
- Demonstrar implementação prática de comunicação via sockets
- Desenvolver uma aplicação cliente-servidor segura
- Explorar técnicas de transferência de arquivos em redes locais
- Aplicar conceitos de segurança em comunicações de rede

## 🌟 Recursos e Conceitos Técnicos

### 🔐 Segurança de Rede
- **Sanitização Avançada**: Proteção contra injeção de comandos
- **Validação Rigorosa de Entrada**: Bloqueia caracteres especiais
- **Proteção contra Path Traversal**: Previne acesso não autorizado
- **Tratamento Controlado de Erros**: Mensagens de erro seguras

### 🚀 Funcionalidades Implementadas
- Listar arquivos
- Enviar arquivos
- Baixar arquivos
- Excluir arquivos

## 📦 Requisitos Técnicos

### Ambiente de Desenvolvimento
- **Linguagem**: Python 3.7+
- **Sistemas Operacionais Compatíveis**: 
  - Windows 10/11
  - macOS 10.14+
  - Linux (Ubuntu 18.04+)

### Bibliotecas Utilizadas
- `socket`: Comunicação de rede
- `os`: Manipulação de arquivos e sistemas
- `sys`: Interações com o sistema
- `json`: Formatação de respostas
- `re`: Validação e sanitização de entrada

## 🔧 Configuração e Instalação

### Preparação do Ambiente
```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/ftpplus.git
cd ftpplus

# Configurar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Ativar ambiente virtual
```

## 💻 Execução do Projeto

### Iniciar Servidor
```bash
python servidor.py
```

### Executar Cliente
```bash
# Sintaxe geral
python client.py <host> <comando>

# Exemplos:
python client.py localhost "listar"
python client.py localhost "enviar arquivo.txt"
python client.py localhost "excluir arquivo.txt"
python client.py localhost "download arquivo.txt"
```

## 🔬 Aspectos Técnicos Detalhados

### Arquitetura de Rede
- **Protocolo**: Socket TCP/IP
- **Porta Padrão**: 12345
- **Escopo**: Rede local
- **Modelo**: Cliente-Servidor

### Características de Implementação
- Comunicação via sockets
- Transferência segura de arquivos
- Tratamento de erros de rede
- Validação de entrada

## 📋 Exemplos de Comunicação

### Resposta de Sucesso
```json
{
  "status": "success", 
  "message": "arquivo.txt enviado com sucesso",
  "timestamp": "2024-02-03T15:30:45Z"
}
```

### Resposta de Erro
```json
{
  "status": "error", 
  "message": "Arquivo não encontrado",
  "code": 404
}
```

## ⚠️ Limitações do Projeto

### Restrições Atuais
- Funcionamento em rede local
- Sem autenticação avançada
- Transferências limitadas a 1GB
- Sem suporte a transferências simultâneas

## 🎓 Aprendizados Acadêmicos

### Conceitos Explorados
- Programação de sockets
- Protocolos de comunicação
- Segurança em redes
- Tratamento de conexões
- Manipulação de arquivos em rede

## 📄 Licença
Projeto acadêmico para disciplina de Redes de Computadores

**Nota**: Desenvolvido exclusivamente para fins educacionais, não recomendado para uso em produção sem adaptações.

## 🏷️ Versão
`v1.0.0` - Versão inicial do trabalho acadêmico