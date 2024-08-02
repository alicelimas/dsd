import Pyro4

@Pyro4.expose
class ReservaDeSalas:
    def __init__(self):
        self.salas = {"Sala 1": True, "Sala 2": True, "Sala 3": True, "Sala 4": True}
        self.reservas = {}
        self.clientes = {}

    def registrar_cliente(self, nome_usuario):
        if nome_usuario in self.clientes:
            return "Nome de usuário já existe."
        self.clientes[nome_usuario] = True
        print(f"Cliente registrado: {nome_usuario}")
        return "Registrado com sucesso."

    def desregistrar_cliente(self, nome_usuario):
        if nome_usuario in self.clientes:
            del self.clientes[nome_usuario]
            print(f"Cliente desregistrado: {nome_usuario}")

    def reservar_sala(self, nome_sala, usuario):
        if not self.salas.get(nome_sala):
            return "Sala já reservada."
        if self.reservas.get(nome_sala) == usuario:
            return "Você já reservou essa sala."
        self.salas[nome_sala] = False
        self.reservas[nome_sala] = usuario
        return "Sala reservada com sucesso."

    def cancelar_reserva(self, nome_sala, usuario):
        if self.reservas.get(nome_sala) != usuario:
            return "Você não tem uma reserva para essa sala."
        self.salas[nome_sala] = True
        del self.reservas[nome_sala]
        return "Reserva cancelada com sucesso."

    def obter_salas(self):
        return self.salas

def main():
    host = "10.3.5.11" 
    daemon = Pyro4.Daemon(host=host)
    ns = Pyro4.locateNS()
    uri = daemon.register(ReservaDeSalas())
    ns.register("reserva.salas", uri)
    print(f"Servidor de reservas iniciado.\nURI: {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
