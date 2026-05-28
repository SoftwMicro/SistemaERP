import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.pedido_controller import PedidoController
from utils.messages import Messages
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController


class PedidoView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = PedidoController()
        self.create_widgets()

    def create_widgets(self):
        # Seleção de cliente
        cliente_frame = ttk.LabelFrame(self.parent, text="Cliente")
        cliente_frame.pack(fill='x', padx=10, pady=5)
        self.cliente_id_var = tk.StringVar()
        ttk.Label(cliente_frame, text="ID ou CPF/CNPJ:").pack(side='left')
        ttk.Entry(cliente_frame, textvariable=self.cliente_id_var, width=20).pack(side='left', padx=5)
        ttk.Button(cliente_frame, text="Selecionar", command=self.selecionar_cliente).pack(side='left')
        self.cliente_nome_label = ttk.Label(cliente_frame, text="")
        self.cliente_nome_label.pack(side='left', padx=10)

        # Seleção de produto
        produto_frame = ttk.LabelFrame(self.parent, text="Adicionar Produto")
        produto_frame.pack(fill='x', padx=10, pady=5)
        self.produto_id_var = tk.StringVar()
        self.quantidade_var = tk.IntVar(value=1)
        ttk.Label(produto_frame, text="ID do Produto:").pack(side='left')
        ttk.Entry(produto_frame, textvariable=self.produto_id_var, width=10).pack(side='left', padx=5)
        ttk.Label(produto_frame, text="Quantidade:").pack(side='left')
        ttk.Entry(produto_frame, textvariable=self.quantidade_var, width=5).pack(side='left', padx=5)
        ttk.Button(produto_frame, text="Adicionar ao Carrinho", command=self.adicionar_produto).pack(side='left')

        # Carrinho
        carrinho_frame = ttk.LabelFrame(self.parent, text="Carrinho de Compras")
        carrinho_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.carrinho_tree = ttk.Treeview(carrinho_frame, columns=("produto_id", "nome", "quantidade", "preco_unitario", "subtotal"), show='headings')
        for col in self.carrinho_tree['columns']:
            self.carrinho_tree.heading(col, text=col)
        self.carrinho_tree.pack(fill='both', expand=True)
        ttk.Button(carrinho_frame, text="Remover Selecionado", command=self.remover_produto).pack(pady=5)

        # Total e ações
        total_frame = ttk.Frame(self.parent)
        total_frame.pack(fill='x', padx=10, pady=5)
        self.total_label = ttk.Label(total_frame, text="Total: R$ 0.00")
        self.total_label.pack(side='left')
        ttk.Label(total_frame, text="Observações:").pack(side='left', padx=5)
        self.obs_var = tk.StringVar()
        ttk.Entry(total_frame, textvariable=self.obs_var, width=30).pack(side='left')
        ttk.Button(total_frame, text="Finalizar Pedido", command=self.finalizar_pedido).pack(side='left', padx=5)

    def selecionar_cliente(self):
        conteudo = self.cliente_id_var.get().strip()
        if not conteudo:
            messagebox.showerror("Erro", Messages.ERRO_ENTRY)
            self.cliente_id_var.set("")

        controller = ClienteController()
        filtro = self.cliente_id_var.get()
        cliente = None
        if filtro.isdigit():
            cliente = controller.pesquisar_clientes(filtro)
            cliente = cliente[0] if cliente else None
        else:
            cliente = controller.pesquisar_clientes(filtro)
            cliente = cliente[0] if cliente else None
        if cliente:
            self.controller.selecionar_cliente(cliente)
            self.cliente_nome_label.config(text=f"Selecionado: {cliente['nome']}")
        else:
            self.cliente_nome_label.config(text=f"")
            messagebox.showerror("Erro", Messages.ERROR_NO_CLIENT)
            


    def adicionar_produto(self):
        controller = ProdutoController()
        produto_id = self.produto_id_var.get()
        try:
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showerror("Erro", "ID do produto inválido.")
            return
        produtos = controller.listar_produtos_disponiveis()
        produto = next((p for p in produtos if p['id'] == produto_id), None)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        quantidade = self.quantidade_var.get()
        msg = self.controller.adicionar_produto(produto, quantidade)
        self.atualizar_carrinho()
        self.total_label.config(text=f"Total: R$ {self.controller.valor_total():.2f}")
        messagebox.showinfo("Info", msg)

    def remover_produto(self):
        selected = self.carrinho_tree.selection()
        if not selected:
            return
        item = self.carrinho_tree.item(selected[0])
        produto_id = item['values'][0]
        self.controller.remover_produto(produto_id)
        self.atualizar_carrinho()
        self.total_label.config(text=f"Total: R$ {self.controller.valor_total():.2f}")

    def atualizar_carrinho(self):
        for i in self.carrinho_tree.get_children():
            self.carrinho_tree.delete(i)
        for item in self.controller.carrinho:
            preco_unitario = f"R$ {item['preco_unitario']:.2f}"
            subtotal = f"R$ {item['subtotal']:.2f}"
            self.carrinho_tree.insert('', 'end', values=(item['produto_id'], item['nome'], item['quantidade'], preco_unitario, subtotal))

    def finalizar_pedido(self):
        usuario = "usuario_pos"  # Substituir por autenticação real se necessário
        obs = self.obs_var.get()
        sucesso, msg = self.controller.finalizar_pedido(obs, usuario)
        if sucesso:
            self.atualizar_carrinho()
            self.total_label.config(text=f"Total: R$ 0.00")
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)


    def obter_pedido_id_dialogo(self):
        return simpledialog.askinteger("Pedido", "Informe o ID do pedido:")
