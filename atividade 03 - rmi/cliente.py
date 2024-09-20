import Pyro4
import tkinter as tk
from tkinter import simpledialog, messagebox

@Pyro4.expose
class ResourceClient:
    def __init__(self):
        self.server = None
        self.username = simpledialog.askstring("Usuário", "Digite seu nome de usuário:")
        self.server_uri = simpledialog.askstring("Servidor", "Digite a URI do servidor:")

        if self.server_uri and self.username:
            try:
                self.server = Pyro4.Proxy(self.server_uri)
                self.server.register_client(self.username)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
                return

        self.root = tk.Tk()
        self.root.title(f"Reserva de Salas - {self.username}")

        # Definir o tamanho da janela
        self.root.geometry("600x400")
        self.root.resizable(False, False)  # Impede redimensionamento da janela

        self.resource_var = tk.StringVar()

        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        self.title_label = tk.Label(self.main_frame, text="Gerenciamento de Salas", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame para listar os recursos
        self.resources_frame = tk.Frame(self.main_frame)
        self.resources_frame.pack(pady=10)

        # Botões para reservar, cancelar reserva e atualizar recursos
        self.reserve_button = tk.Button(self.main_frame, text="Reservar Sala", command=self.reserve_resource)
        self.reserve_button.pack(pady=5)

        self.cancel_button = tk.Button(self.main_frame, text="Cancelar Reserva", command=self.cancel_reservation)
        self.cancel_button.pack(pady=5)

        self.update_button = tk.Button(self.main_frame, text="Atualizar Recursos", command=self.update_resources)
        self.update_button.pack(pady=5)

        self.update_resources()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def reserve_resource(self):
        resource_name = self.resource_var.get()
        if resource_name and self.server:
            result = self.server.reserve_resource(resource_name, self.username)
            messagebox.showinfo("Resultado", result)
            self.update_resources()

    def cancel_reservation(self):
        resource_name = self.resource_var.get()
        if resource_name and self.server:
            result = self.server.cancel_reservation(resource_name, self.username)
            messagebox.showinfo("Resultado", result)
            self.update_resources()

    def update_resources(self):
        if self.server:
            try:
                resources = self.server.get_resources()
                self.resource_var.set(None)

                for widget in self.resources_frame.winfo_children():
                    widget.destroy()

                for resource, available in resources.items():
                    status = "Disponível" if available else "Indisponível"
                    radio_button = tk.Radiobutton(self.resources_frame, text=f"{resource} - {status}",
                                                 variable=self.resource_var, value=resource)
                    radio_button.pack(anchor="w")

                if resources:
                    self.resource_var.set(next(iter(resources)))

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível atualizar os recursos: {e}")

    def receive_notification(self, message):
        messagebox.showinfo("Notificação", message)

    def on_closing(self):
        if self.server:
            self.server.unregister_client(self.username)
        self.root.destroy()

def run_client():
    ResourceClient()

if __name__ == "__main__":
    run_client()
