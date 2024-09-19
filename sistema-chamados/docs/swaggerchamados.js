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