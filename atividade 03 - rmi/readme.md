# Projeto RMI

Um sistema simples para reserva de salas, utilizando Pyro4 para comunicação entre o servidor e os clientes. O sistema permite que múltiplos usuários reservem e cancelem reservas de salas.

## Estrutura do Projeto

- `servidor.py`: Implementação do servidor em Python.
- `cliente.py`: Implementação do cliente em Python.

## Tecnologias Utilizadas

- **Python 3**
- **Pyro4** (para comunicação remota)
- **Tkinter** (para interface gráfica).

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python** (versão 3.6 ou superior)

## Configuração do Servidor

Antes de instalar as dependências, certifique-se de estar no diretório de atividade 03 - rmi.
```
cd .dsd\atividade 03 - rmi\
```

1. **Instale as dependências do Python:**

   Crie um ambiente virtual e instale as bibliotecas necessárias com `pip`:

   ```
   python -m venv venv
   venv\Scripts\activate - para ativar a venv
   pip install Pyro4
   ```
   
2. **Inicie o Name Server do Pyro4:**
    ```
   python -m Pyro4.naming
    ```
3. **Inicie o servidor:**
    ```
    python servidor.py
    ```
## Configuração do Cliente

1. **Instale as dependências necessárias:**

   Como já temos a máquina virtual criada, podemos usá-la, abrindo um novo terminal e ativando-a:

   ```
   venv\Scripts\activate - para ativar a venv
   ```
   Caso ainda não tenha criado uma máquina virtual, crie-a conforme descrito para a configuração do servidor, ative-a e faça a instalação do Pyro4.
  
2. **Execute o cliente:**
    ```
    python cliente.py
