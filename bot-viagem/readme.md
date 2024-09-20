# Projeto SOAP para Bot-Viagem

Este projeto demonstra a comunicação entre um cliente JavaScript e um servidor Python utilizando SOAP, para buscar destinos com base no tipo de viagem e fornecer dicas sobre as cidades selecionadas.

## Estrutura do Projeto

- `server.py`: Implementação do servidor SOAP em Python.
- `cliente.js`: Implementação do cliente SOAP em JavaScript.

## Tecnologias Utilizadas

- **Node.js**: Para implementar o cliente que consome o serviço SOAP.
- **Python**: Para criar o servidor SOAP utilizando a biblioteca Spyne.
- **Spyne**: Biblioteca para construção de serviços web SOAP em Python.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python** (versão 3.6 ou superior)
- **Node.js** (versão 14 ou superior)

## Configuração do Servidor

Antes de instalar as dependências, certifique-se de estar no diretório de bot-viagem.
```
cd .dsd\bot-viagem\
```

1. **Instale as dependências do Python:**

   Crie um ambiente virtual e instale as bibliotecas necessárias com `pip`:

   ```
   python -m venv venv
   venv\Scripts\activate - para ativar a venv
   pip install -r requirements.txt

2. **Inicie o servidor:**

    python main.py

## Configuração do Cliente

1. **Instale as dependências necessárias:**

   Navegue até o diretório onde o `cliente.js` está localizado e instale os pacotes necessários com o `npm`:

   ```
   npm install soap readline
  
2. **Execute o cliente:**
    ```
    node cliente.js
    ```
  -  Link para apresentação no [Canva](https://www.canva.com/design/DAGRTVjpwcU/DCAY1Fw47TTrLaLcbH3KZg/edit?utm_content=DAGRTVjpwcU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
