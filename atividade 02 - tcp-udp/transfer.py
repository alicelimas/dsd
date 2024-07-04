import tkinter as tk
from tkinter import filedialog, messagebox 
from tkinter import ttk
import threading 
import socket 
import os 

# Tamanho máximo do pacote UDP
UDP_PACKET_SIZE = 1024

# Variáveis globais para controle do servidor
server_tcp_running = False
server_udp_running = False

# Função para iniciar o servidor TCP
def start_tcp_server():
    global server_tcp_running
    if not server_tcp_running:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            server.bind(("0.0.0.0", 9999)) 
            server.listen(5) 
            print("Servidor TCP esperando por conexões...")

            while True:
                client_socket, addr = server.accept() 
                print(f"Conexão de {addr} estabelecida.")
                file_data = b""
                while True:
                    data = client_socket.recv(1024) 
                    if not data:
                        break
                    file_data += data
                file_name, file_content = process_received_data(file_data)
                save_file(file_name, file_content)
                client_socket.close()
        except Exception as e:
            print(f"Erro no Servidor TCP: {e}")
        finally:
            server_tcp_running = False

# Função para iniciar o servidor UDP
def start_udp_server():
    global server_udp_running
    if not server_udp_running:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            server.bind(("0.0.0.0", 9999))
            print("Servidor UDP esperando por dados...")

            file_data = {}
            expected_packets = 0
            received_packets = 0
            file_name = None

            while True:
                data, addr = server.recvfrom(UDP_PACKET_SIZE + 100)
                if data:
                    try:
                        parts = data.split(b'|')
                        if len(parts) < 4:
                            raise ValueError("Cabeçalho incompleto")

                        if file_name is None:
                            file_name = parts[0].decode()
                            total_packets = int(parts[1].decode())
                            expected_packets = total_packets

                        seq_num = int(parts[2].decode())
                        file_data[seq_num] = parts[3]

                        received_packets = len(file_data)
                        if received_packets == expected_packets:
                            ordered_data = b''.join(file_data[i] for i in range(expected_packets))
                            save_file(file_name, ordered_data)
                            print(f"Arquivo '{file_name}' recebido e salvo com sucesso pelo UDP.")
                            break

                    except ValueError as ve:
                        print(f"Erro ao processar cabeçalho UDP: {ve}")
                        continue

        except Exception as e:
            print(f"Erro no Servidor UDP: {e}")
        finally:
            server_udp_running = False

# Função para processar os dados recebidos (extrair nome do arquivo e conteúdo)
def process_received_data(data):
    file_name, file_content = data.split(b'|', 1)
    return file_name.decode(), file_content

# Função para salvar o arquivo recebido
def save_file(file_name, file_data):
    try:
        save_dir = "received_files"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(file_data)
        print(f"Arquivo '{file_name}' recebido e salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Função para iniciar o cliente TCP
def start_tcp_client(file_path):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 9999))
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path).encode()
            client.sendall(file_name + b'|' + file_data)
        client.close()
        print("Arquivo enviado com sucesso pelo TCP!")
    except Exception as e:
        print(f"Erro no Cliente TCP: {e}")

# Função para iniciar o cliente UDP
def start_udp_client(file_path):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path).encode()
            total_packets = (len(file_data) + UDP_PACKET_SIZE - 1) // UDP_PACKET_SIZE

            for i in range(total_packets):
                start = i * UDP_PACKET_SIZE
                end = start + UDP_PACKET_SIZE
                packet = file_data[start:end]
                header = f"{file_name.decode()}|{total_packets}|{i}|".encode()
                client.sendto(header + packet, ("127.0.0.1", 9999))

        print("Arquivo enviado com sucesso pelo UDP!")
    except Exception as e:
        print(f"Erro no Cliente UDP: {e}")

# Função para selecionar o arquivo
def select_file():
    file_path = filedialog.askopenfilename() 
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Função para iniciar a transmissão
def start_transmission():
    protocol = protocol_var.get()
    file_path = file_entry.get() 

    if not file_path:
        messagebox.showwarning("Aviso", "Selecione um arquivo para enviar.")
        return

    if protocol == "TCP":
        threading.Thread(target=start_tcp_client, args=(file_path,)).start() 
    elif protocol == "UDP":
        threading.Thread(target=start_udp_client, args=(file_path,)).start() 

# Interface gráfica com tkinter e ttk
root = tk.Tk()
root.title("Transmissão de Arquivos")

style = ttk.Style()
style.configure("TFrame", padding=10)
style.configure("TButton", padding=5)
style.configure("TLabel", padding=5)
style.configure("TRadiobutton", padding=5)

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10)

file_frame = ttk.Frame(main_frame)
file_frame.grid(row=0, column=0, pady=10, sticky="ew")

file_label = ttk.Label(file_frame, text="Arquivo:")
file_label.grid(row=0, column=0, padx=5, sticky="w")

file_entry = ttk.Entry(file_frame, width=50)
file_entry.grid(row=0, column=1, padx=5, sticky="ew")

file_button = ttk.Button(file_frame, text="Selecionar", command=select_file)
file_button.grid(row=0, column=2, padx=5, sticky="e")

file_frame.columnconfigure(1, weight=1)

protocol_frame = ttk.Frame(main_frame)
protocol_frame.grid(row=1, column=0, pady=10, sticky="ew")

protocol_label = ttk.Label(protocol_frame, text="Protocolo:")
protocol_label.grid(row=0, column=0, padx=5, sticky="w")

protocol_var = tk.StringVar(value="TCP")
tcp_radio = ttk.Radiobutton(protocol_frame, text="TCP", variable=protocol_var, value="TCP")
tcp_radio.grid(row=0, column=1, padx=5, sticky="w")
udp_radio = ttk.Radiobutton(protocol_frame, text="UDP", variable=protocol_var, value="UDP")
udp_radio.grid(row=0, column=2, padx=5, sticky="w")

transmit_button = ttk.Button(main_frame, text="Iniciar Transmissão", command=start_transmission)
transmit_button.grid(row=2, column=0, pady=20)

main_frame.columnconfigure(0, weight=1)

# Iniciar o servidor em uma thread separada
threading.Thread(target=start_tcp_server, daemon=True).start()
threading.Thread(target=start_udp_server, daemon=True).start()

root.mainloop()
