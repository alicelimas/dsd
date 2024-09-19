const express = require('express');
const axios = require('axios');
const swaggerJsDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const WebSocket = require('ws');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

const PORT = 3000;

// Configuração do Swagger
const swaggerOptions = {
  swaggerDefinition: {
    openapi: '3.0.0',
    info: {
      title: 'API Gateway para Sistema de Chamados',
      description: 'APIs para gerenciamento de chamados e usuários',
      version: '1.0.0',
    },
  },
  apis: ['gateway.js'],
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

/**
 * @swagger
 * /api/chamados:
 *   get:
 *     description: Obtém uma lista de todos os chamados
 *     responses:
 *       200:
 *         description: Lista de chamados
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 chamados:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: integer
 *                       descricao:
 *                         type: string
 *                       status:
 *                         type: string
 *                 _links:
 *                   type: object
 *                   properties:
 *                     self:
 *                       type: object
 *                       properties:
 *                         href:
 *                           type: string
 *                     criar:
 *                       type: object
 *                       properties:
 *                         href:
 *                           type: string
 */
app.get('/api/chamados', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:4000/chamados');
    res.json({
      chamados: response.data,
      _links: {
        self: { href: '/api/chamados' },
        criar: { href: '/api/chamados/criar' },
      },
    });
  } catch (error) {
    res.status(500).json({ erro: 'Erro ao buscar chamados' });
  }
});

/**
 * @swagger
 * /api/usuarios:
 *   get:
 *     description: Obtém uma lista de todos os usuários
 *     responses:
 *       200:
 *         description: Lista de usuários
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 usuarios:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: integer
 *                       name:
 *                         type: string
 *                       email:
 *                         type: string
 *                 _links:
 *                   type: object
 *                   properties:
 *                     self:
 *                       type: object
 *                       properties:
 *                         href:
 *                           type: string
 *                     criar:
 *                       type: object
 *                       properties:
 *                         href:
 *                           type: string
 */
app.get('/api/usuarios', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:4001/usuarios');
    res.json({
      usuarios: response.data,
      _links: {
        self: { href: '/api/usuarios' },
        criar: { href: '/api/usuarios/criar' },
      },
    });
  } catch (error) {
    res.status(500).json({ erro: 'Erro ao buscar usuários' });
  }
});

/**
 * @swagger
 * /api/chamados/criar:
 *   post:
 *     description: Cria um novo chamado com um usuário associado
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               descricao:
 *                 type: string
 *               usuarioId:
 *                 type: integer
 *                 description: ID do usuário associado ao chamado
 *     responses:
 *       201:
 *         description: Chamado criado com sucesso
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: integer
 *                 descricao:
 *                   type: string
 *                 status:
 *                   type: string
 *                 usuarioId:
 *                   type: integer
 *                   description: ID do usuário associado ao chamado
 */
app.post('/api/chamados/criar', async (req, res) => {
  try {
    const { descricao, usuarioId } = req.body;

    // Enviar a requisição para a API de Chamados
    const response = await axios.post('http://localhost:4000/chamados/criar', {
      descricao,
      usuarioId,  // Inclui o ID do usuário associado ao chamado
    });

    res.status(201).json(response.data);

    // Notificar todos os clientes WebSocket sobre o novo chamado
    notificarClientes(JSON.stringify(response.data));
  } catch (error) {
    res.status(500).json({ erro: 'Erro ao criar chamado' });
  }
});

/**
 * @swagger
 * /api/chamados/{id}/atualizar:
 *   put:
 *     description: Atualiza o status de um chamado
 *     parameters:
 *       - name: id
 *         in: path
 *         required: true
 *         description: ID do chamado a ser atualizado
 *         schema:
 *           type: integer
 *       - name: status
 *         in: body
 *         required: true
 *         description: Novo status do chamado
 *         schema:
 *           type: object
 *           properties:
 *             status:
 *               type: string
 *     responses:
 *       200:
 *         description: Status do chamado atualizado
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: integer
 *                 descricao:
 *                   type: string
 *                 status:
 *                   type: string
 */
app.put('/api/chamados/:id/atualizar', async (req, res) => {
  try {
    const id = req.params.id;
    const status = req.body.status;
    const response = await axios.put(`http://localhost:4000/chamados/${id}/atualizar`, { status });
    res.json(response.data);

    console.log('Atualização de chamado recebida:', response.data);

    // Notificar todos os clientes WebSocket sobre a atualização do status
    notificarClientes(JSON.stringify(response.data));
  } catch (error) {
    res.status(500).json({ erro: 'Erro ao atualizar status do chamado' });
  }
});

/**
 * @swagger
 * /notificar:
 *   post:
 *     description: Recebe notificações de novos chamados e notifica os clientes WebSocket
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               descricao:
 *                 type: string
 *     responses:
 *       200:
 *         description: Notificação recebida com sucesso
 */
app.post('/notificar', (req, res) => {
  const novoChamado = req.body;
  console.log('Notificação de novo chamado recebida:', novoChamado);
  notificarClientes(JSON.stringify(novoChamado)); // Notifica todos os clientes WebSocket
  res.sendStatus(200);
});

/**
 * @swagger
 * /api/chamados/{id}/deletar:
 *   delete:
 *     description: Deleta um chamado pelo ID
 *     parameters:
 *       - name: id
 *         in: path
 *         required: true
 *         description: ID do chamado a ser deletado
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Chamado deletado com sucesso
 *       404:
 *         description: Chamado não encontrado
 */
app.delete('/api/chamados/:id/deletar', async (req, res) => {
  try {
    const id = req.params.id;

    // Enviar a requisição para a API de Chamados
    const response = await axios.delete(`http://localhost:4000/chamados/${id}`);

    if (response.status === 200) {
      res.status(200).json({ mensagem: 'Chamado deletado com sucesso' });
      console.log('Exclusão de chamado recebida:', response.data);
      // Notificar os clientes WebSocket sobre o chamado deletado
      notificarClientes(JSON.stringify({ id, acao: 'deletar' }));
    } else {
      res.status(404).json({ erro: 'Chamado não encontrado' });
    }
  } catch (error) {
    res.status(500).json({ erro: 'Erro ao deletar chamado' });
  }
});


// Inicializando o servidor
app.listen(PORT, () => {
  console.log(`API Gateway rodando na porta ${PORT}`);
});

// Servidor WebSocket
const wss = new WebSocket.Server({ port: 8080 });

let clientes = [];

wss.on('connection', (ws) => {
  console.log('Cliente conectado via WebSocket');
  clientes.push(ws);

  ws.on('message', (message) => {
    console.log('Mensagem recebida:', message);
  });

  ws.on('close', () => {
    console.log('Cliente desconectado');
    clientes = clientes.filter(cliente => cliente !== ws);
  });

  ws.send('Conexão WebSocket estabelecida');
});

// Função para notificar todos os clientes conectados
function notificarClientes(mensagem) {
  clientes.forEach(cliente => {
    cliente.send(mensagem);
  });
}
