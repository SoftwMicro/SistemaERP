import tkinter as tk
from tkinter import ttk
from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ClienteController()
        self.create_widgets()

    def create_widgets(self):
        self.search_var = tk.StringVar()
        search_frame = ttk.Frame(self.parent)
        search_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(search_frame, text="Buscar Cliente (CPF/CNPJ ou Nome):").pack(side='left')
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side='left', padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_clientes).pack(side='left')

        self.tree = ttk.Treeview(self.parent, columns=("id", "nome", "cpf_cnpj", "email", "telefone", "ativo"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

    def buscar_clientes(self):
        filtro = self.search_var.get()
        clientes = self.controller.pesquisar_clientes(filtro)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for c in clientes:
           self.tree.insert('', 'end', values=(c['id'], c['nome'], c['cpf_cnpj'], c['email'], c['telefone'], c['ativo']))
