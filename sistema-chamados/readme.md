# Sistema de Chamados com Websocket e API Gateway

Este projeto é uma implementação de um sistema de gerenciamento de chamados, utilizando um API Gateway para centralizar as requisições e WebSocket para atualizações em tempo real. O sistema permite que usuários criem, atualizem e gerenciem chamados de forma eficiente.

## Estrutura do Projeto

- **API Gateway**: Centraliza as requisições e integra diferentes serviços.
- **Serviço de Chamados**:  Gerencia a criação, atualização, listagem e exclusão de chamados.
- **Serviço de Usuários**:  Gerencia a criação, atualização, listagem e exclusão de usuários.
- **WebSocket**: Proporciona comunicação em tempo real entre o cliente e o servidor.

## Tecnologias Utilizadas

- **Node.js**
- **Express** (para o API Gateway)
- **Swagger** (para documentação da API)
- **WebSocket** (para comunicação em tempo real)

## Requisitos

- **Node.js (versão 14 ou superior)**
- **npm** (gerenciador de pacotes do Node.js).

## Instalação

### 1. Clonar o Repositório

```
git clone https://github.com/alicelimas/dsd/tree/main/sistema-chamados
cd dsd/sistema-chamados
```
### 2. Instalar Dependências
```
npm install express
```

### 3. Executar 
```
node gateway.js

cd dsd/sistema-chamados/api-chamados
node server.js

cd cd dsd/sistema-chamados/api-usuarios
node server.js
```

### 4. Acessar a Documentação da API
Abra seu navegador para visualizar a documentação gerada pelo Swagger.
```
http://localhost:3000/api-docs
```

### 5. Acessar a Interface Web
Abra o arquivo no seu navegador para interagir com o sistema.
```
index.html 
```

### 6. Enviar Chamados via API

- Você pode usar curl ou Postman para enviar requisições à API. Por exemplo, para criar um novo chamado:
```
curl -X POST http://localhost:3000/api/chamados/criar -H "Content-Type: application/json" -d '{"descricao": "Problema na impressora", "usuarioId": 1}'
```
