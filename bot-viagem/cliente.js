const soap = require('soap');
const readline = require('readline');

const url = 'http://192.168.1.18:8000/?wsdl'; // Altere conforme necessário

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Função para buscar destinos
const buscarDestinos = () => {
    rl.question('Qual tipo de destino você deseja? (praia, montanha, cultura): ', function(tipo) {
        rl.question('Qual é o seu orçamento para a viagem? (baixo, médio, alto): ', function(orçamento) {
            rl.question('Quantos dias você pretende viajar? ', function(dias) {
                soap.createClient(url, function(err, client) {
                    if (err) {
                        console.error('Erro ao criar cliente SOAP:', err);
                        rl.close();
                        return;
                    }

                    client.buscar_destinos({ tipo: tipo, orçamento: orçamento, dias: dias }, function(err, result) {
                        if (err) {
                            console.error('Erro ao chamar o método SOAP:', err);
                            rl.close();
                            return;
                        }

                        const destinos = result.buscar_destinosResult.string;
                        if (destinos && destinos.length > 0) {
                            console.log('Destinos encontrados: ', destinos.join(', '));

                            rl.question('Escolha uma cidade: ', function(cidade) {
                                client.obter_dicas({ cidade: cidade }, function(err, result) {
                                    if (err) {
                                        console.error('Erro ao chamar o método SOAP:', err);
                                        rl.close();
                                        return;
                                    }
                                    console.log('Dicas para ' + cidade + ':');
                                    console.log(result.obter_dicasResult);
                                    rl.close();
                                });
                            });
                        } else {
                            console.log('Nenhum destino encontrado para o tipo especificado.');
                            rl.close();
                        }
                    });
                });
            });
        });
    });
};

// Iniciar a busca
buscarDestinos();
