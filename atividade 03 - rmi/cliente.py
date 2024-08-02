import Pyro4
import tkinter as tk
from tkinter import simpledialog, messagebox

class ClienteDeSalas:
    def __init__(self):
        self.servidor = None
        self.nome_usuario = simpledialog.askstring("Usuário", "Digite seu nome de usuário:")

        if not self.nome_usuario:
            messagebox.showerror("Erro", "Nome de usuário não pode estar vazio.")
            return

        self.uri_servidor = simpledialog.askstring("Servidor", "Digite a URI do servidor:")

        if not self.uri_servidor:
            messagebox.showerror("Erro", "URI do servidor não pode estar vazio.")
            return

        try:
            self.servidor = Pyro4.Proxy(self.uri_servidor)
            resultado = self.servidor.registrar_cliente(self.nome_usuario)
            if resultado != "Registrado com sucesso.":
                messagebox.showerror("Erro", resultado)
                return
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            return

        self.root = tk.Tk()
        self.root.title(f"Reserva de Salas - {self.nome_usuario}")

        # Definir o tamanho da janela
        self.root.geometry("600x400")
        self.root.resizable(False, False)  # Impede redimensionamento da janela

        self.sala_var = tk.StringVar()

        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        self.title_label = tk.Label(self.main_frame, text="Gerenciamento de Salas", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame para listar as salas
        self.salas_frame = tk.Frame(self.main_frame)
        self.salas_frame.pack(pady=10)

        # Botões para reservar e cancelar reserva
        self.reserve_button = tk.Button(self.main_frame, text="Reservar Sala", command=self.reservar_sala)
        self.reserve_button.pack(pady=5)

        self.cancel_button = tk.Button(self.main_frame, text="Cancelar Reserva", command=self.cancelar_reserva)
        self.cancel_button.pack(pady=5)

        self.atualizar_salas_periodicamente()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def reservar_sala(self):
        nome_sala = self.sala_var.get()
        if nome_sala and self.servidor:
            resultado = self.servidor.reservar_sala(nome_sala, self.nome_usuario)
            messagebox.showinfo("Resultado", resultado)
            self.atualizar_salas()

    def cancelar_reserva(self):
        nome_sala = self.sala_var.get()
        if nome_sala and self.servidor:
            resultado = self.servidor.cancelar_reserva(nome_sala, self.nome_usuario)
            messagebox.showinfo("Resultado", resultado)
            self.atualizar_salas()

    def atualizar_salas(self):
        if self.servidor:
            try:
                salas = self.servidor.obter_salas()
                self.sala_var.set(None)

                for widget in self.salas_frame.winfo_children():
                    widget.destroy()

                for sala, disponivel in salas.items():
                    status = "Disponível" if disponivel else "Indisponível"
                    radio_button = tk.Radiobutton(self.salas_frame, text=f"{sala} - {status}",
                                                  variable=self.sala_var, value=sala)
                    radio_button.pack(anchor="w")

                if salas:
                    self.sala_var.set(next(iter(salas)))

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível atualizar as salas: {e}")

    def atualizar_salas_periodicamente(self):
        self.atualizar_salas()
        self.root.after(4000, self.atualizar_salas_periodicamente)  

    def on_closing(self):
        if self.servidor:
            self.servidor.desregistrar_cliente(self.nome_usuario)
        self.root.destroy()

def run_client():
    ClienteDeSalas()

if __name__ == "__main__":
    run_client()
