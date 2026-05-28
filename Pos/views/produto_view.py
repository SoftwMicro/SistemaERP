import tkinter as tk
from tkinter import ttk
from controllers.produto_controller import ProdutoController

class ProdutoView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProdutoController()
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.parent, columns=("id", "sku", "nome", "preco", "quantidade_estoque", "ativo"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.listar_produtos()

    def listar_produtos(self):
        produtos = self.controller.listar_produtos_disponiveis()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in produtos:
            self.tree.insert('', 'end', values=(p['id'], p['sku'], p['nome'],  f"R$ {p['preco']:.2f}" , p['quantidade_estoque'], p['ativo']))
