const express = require('express');
const app = express();
app.use(express.json());

const PORT = 4001;

let usuarios = [
  { id: 1, nome: 'João Pedro', email: 'joao@gmail.com' },
  { id: 2, nome: 'Maria Clara', email: 'maria@gmail.com' },
];

// Listar usuários
app.get('/usuarios', (req, res) => {
  res.json(usuarios);
});

// Criar um novo usuário
app.post('/usuarios/criar', (req, res) => {
  const novoUsuario = {
    id: usuarios.length + 1,
    nome: req.body.nome,
    email: req.body.email,
  };
  usuarios.push(novoUsuario);
  res.status(201).json(novoUsuario);
});

app.listen(PORT, () => {
  console.log(`API de Usuários rodando na porta ${PORT}`);
});
