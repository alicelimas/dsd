const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const PORT = 4000;

let chamados = [
  { id: 1, descricao: 'Erro no sistema', status: 'aberto', usuarioId: 1 },
  { id: 2, descricao: 'Problema de login', status: 'fechado', usuarioId: 2 },
];

// Função para notificar o API Gateway
async function notificarNovoChamado(chamado) {
  try {
    await axios.post('http://localhost:3000/notificar', chamado);
  } catch (error) {
    console.error('Erro ao notificar API Gateway:', error);
  }
}

// Listar chamados
app.get('/chamados', (req, res) => {
  res.json(chamados);
});

// Criar um novo chamado
app.post('/chamados/criar', async (req, res) => {
  const { descricao, usuarioId } = req.body;
  const novoChamado = {
    id: chamados.length + 1,
    descricao,
    status: 'aberto',
    usuarioId, 
  };
  chamados.push(novoChamado);
  await notificarNovoChamado(novoChamado); // Notificar o API Gateway
  res.status(201).json(novoChamado);
});

// Atualizar status de um chamado
app.put('/chamados/:id/atualizar', (req, res) => {
  const chamadoId = parseInt(req.params.id);
  const chamado = chamados.find(c => c.id === chamadoId);
  if (chamado) {
    chamado.status = req.body.status;
    res.json(chamado);
  } else {
    res.status(404).json({ erro: 'Chamado não encontrado' });
  }
});

// Deletar um chamado
app.delete('/chamados/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = chamados.findIndex(ch => ch.id === id);

  if (index !== -1) {
    chamados.splice(index, 1);
    res.status(200).json({ mensagem: 'Chamado deletado com sucesso' });
  } else {
    res.status(404).json({ erro: 'Chamado não encontrado' });
  }
});

app.listen(PORT, () => {
  console.log(`API de Chamados rodando na porta ${PORT}`);
});
