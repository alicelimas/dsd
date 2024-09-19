from spyne import Application, rpc, ServiceBase, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import unicodedata

# Função para normalizar strings
def normalizar_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

# Simulação de dados
destinos = {
    "praia": ["Rio de Janeiro", "Fortaleza", "Salvador", "Florianópolis"],
    "montanha": ["Gramado", "Campos do Jordão", "Teresópolis", "Petrópolis"],
    "cultura": ["São Paulo", "Belo Horizonte", "Olinda", "Ouro Preto"]
}

dicas = {
    "Rio de Janeiro": "Visite o Cristo Redentor e as praias de Copacabana.",
    "Fortaleza": "Aproveite o Beach Park, a praia de Iracema e a culinária local.",
    "Salvador": "Conheça o Pelourinho e o Elevador Lacerda.",
    "Gramado": "Não perca o Natal Luz e a Rua Coberta.",
    "Campos do Jordão": "Explore o Horto Florestal e o centro da cidade.",
    "Teresópolis": "Visite o Parque Nacional da Serra dos Órgãos.",
    "São Paulo": "Descubra a Avenida Paulista, o MASP e o Parque Ibirapuera.",
    "Belo Horizonte": "Experimente o pão de queijo e visite o Mercado Central.",
    "Olinda": "Aprecie o Carnaval e as ladeiras históricas.",
    "Ouro Preto": "Explore as igrejas barrocas, como a Igreja de São Francisco de Assis, e aproveite para visitar os museus da cidade.",
    "Florianópolis": "Não deixe de visitar a Praia da Joaquina e a Lagoa da Conceição. Experimente a culinária local, como as ostras.",
    "Petrópolis": "Visite o Museu Imperial e a Catedral de São Pedro de Alcântara. Aproveite o clima ameno e as trilhas nas montanhas ao redor."
}

class BotViagemService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns=Array(Unicode))
    def buscar_destinos(ctx, tipo, orçamento, dias):
        tipo_normalizado = normalizar_string(tipo)
        destinos_filtrados = []

        # Verifica se o tipo normalizado existe nas chaves
        for key in destinos.keys():
            if normalizar_string(key) == tipo_normalizado:
                destinos_filtrados = destinos[key]
                break

        return destinos_filtrados

    @rpc(Unicode, _returns=Unicode)
    def obter_dicas(ctx, cidade):
        cidade_normalizada = normalizar_string(cidade)
        # Verifica se a cidade normalizada existe nas chaves de dicas
        for key in dicas.keys():
            if normalizar_string(key) == cidade_normalizada:
                return dicas[key]
        return "Não há dicas disponíveis para esta cidade."

# Criação da aplicação SOAP
application = Application(
    [BotViagemService],
    tns='spyne.examples.botviagem',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('192.168.1.18', 8000, wsgi_application)
    print("Servidor escutando em http://192.168.1.18:8000/?wsdl")
    server.serve_forever()
