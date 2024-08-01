import Pyro4

@Pyro4.expose
class ReservaDeSalas:
    def __init__(self):
        self.salas = {"Sala 1": True, "Sala 2": True, "Sala 3": True, "Sala 4": True}
        self.reservas = {}
        self.clientes = []

    def registrar_cliente(self, cliente_uri):
        if cliente_uri not in self.clientes:
            self.clientes.append(cliente_uri)
            print(f"Cliente registrado: {cliente_uri}")

    def desregistrar_cliente(self, cliente_uri):
        if cliente_uri in self.clientes:
            self.clientes.remove(cliente_uri)
            print(f"Cliente desregistrado: {cliente_uri}")

    def reservar_sala(self, nome_sala, usuario):
        if not self.salas.get(nome_sala):
            return "Sala já reservada."
        if self.reservas.get(nome_sala) == usuario:
            return "Você já reservou essa sala."
        self.salas[nome_sala] = False
        self.reservas[nome_sala] = usuario
        self.notificar_clientes(f"{usuario} reservou {nome_sala}.")
        return "Sala reservada com sucesso."

    def cancelar_reserva(self, nome_sala, usuario):
        if self.reservas.get(nome_sala) != usuario:
            return "Você não tem uma reserva para essa sala."
        self.salas[nome_sala] = True
        del self.reservas[nome_sala]
        self.notificar_clientes(f"{usuario} cancelou a reserva de {nome_sala}.")
        return "Reserva cancelada com sucesso."

    def obter_salas(self):
        return self.salas

    def notificar_clientes(self, mensagem):
        for cliente_uri in self.clientes:
            try:
                cliente = Pyro4.Proxy(cliente_uri)
                cliente.receber_notificacao(mensagem)
            except Exception as e:
                print(f"Erro ao notificar cliente {cliente_uri}: {e}")

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
