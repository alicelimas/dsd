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

// Atualizar um usuário
app.put('/usuarios/:id', (req, res) => {
  const usuarioId = parseInt(req.params.id);
  const usuario = usuarios.find(u => u.id === usuarioId);
  
  if (usuario) {
    usuario.nome = req.body.nome;
    usuario.email = req.body.email;
    res.json(usuario);
  } else {
    res.status(404).json({ erro: 'Usuário não encontrado' });
  }
});

// Deletar um usuário
app.delete('/usuarios/:id', (req, res) => {
  const usuarioId = parseInt(req.params.id);
  const index = usuarios.findIndex(u => u.id === usuarioId);
  
  if (index !== -1) {
    usuarios.splice(index, 1);
    res.status(200).json({ mensagem: 'Usuário deletado com sucesso' });
  } else {
    res.status(404).json({ erro: 'Usuário não encontrado' });
  }
});

app.listen(PORT, () => {
  console.log(`API de Usuários rodando na porta ${PORT}`);
});
