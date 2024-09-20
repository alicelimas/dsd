import Pyro4

@Pyro4.expose
class ResourceReservation:
    def __init__(self):
        self.resources = {"Sala 1": True, "Sala 2": True, "Sala 3": True, "Sala 4": True}
        self.reservations = {}
        self.clients = []

    def register_client(self, client_uri):
        if client_uri not in self.clients:
            self.clients.append(client_uri)
            print(f"Cliente registrado: {client_uri}")

    def unregister_client(self, client_uri):
        if client_uri in self.clients:
            self.clients.remove(client_uri)
            print(f"Cliente desregistrado: {client_uri}")

    def reserve_resource(self, resource_name, user):
        if not self.resources.get(resource_name):
            return "Sala já reservada."
        if self.reservations.get(resource_name) == user:
            return "Você já reservou essa sala."
        self.resources[resource_name] = False
        self.reservations[resource_name] = user
        self.notify_clients(f"{user} reservou {resource_name}.")
        return "Sala reservada com sucesso."

    def cancel_reservation(self, resource_name, user):
        if self.reservations.get(resource_name) != user:
            return "Você não tem uma reserva para essa sala."
        self.resources[resource_name] = True
        del self.reservations[resource_name]
        self.notify_clients(f"{user} cancelou a reserva de {resource_name}.")
        return "Reserva cancelada com sucesso."

    def get_resources(self):
        return self.resources

    def notify_clients(self, message):
        for client_uri in self.clients:
            try:
                client = Pyro4.Proxy(client_uri)
                client.receive_notification(message)
            except Exception as e:
                print(f"Erro ao notificar cliente {client_uri}: {e}")

def main():
    host = "10.3.5.12" 
    daemon = Pyro4.Daemon(host=host)
    ns = Pyro4.locateNS()
    uri = daemon.register(ResourceReservation())
    ns.register("resource.reservation", uri)
    print(f"Servidor de reservas iniciado. URI: {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
