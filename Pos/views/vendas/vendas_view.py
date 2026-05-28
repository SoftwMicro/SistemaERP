import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.vendas.vendas_controller import VendasController
from utils.messages import Messages

class VendasView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = VendasController()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(frame, columns=("id", "cliente", "data_criacao", "status", "valor_total"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)
        ttk.Button(frame, text="Cancelar Pedido", command=self.cancelar_pedido).pack(side='left', padx=5, pady=5)
        ttk.Button(frame, text="Deletar Pedido", command=self.deletar_pedido).pack(side='left', padx=5, pady=5)
        ttk.Button(frame, text="Atualizar", command=self.atualizar_lista).pack(side='left', padx=5, pady=5)
        self.atualizar_lista()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        pedidos = self.controller.listar_pedidos()
        for p in pedidos:
            self.tree.insert('', 'end', values=(p['id'], p['cliente'], p['data_criacao'], p['status'], f"R$ {p['valor_total']:.2f}"))

    def cancelar_pedido(self):
        pedido_id = self.obter_pedido_id_selecionado()
        if not pedido_id:
            return
        usuario = "usuario_pos"
        sucesso, msg = self.controller.cancelar_pedido(pedido_id, usuario)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def deletar_pedido(self):
        pedido_id = self.obter_pedido_id_selecionado()
        if not pedido_id:
            return
        sucesso, msg = self.controller.deletar_pedido(pedido_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def obter_pedido_id_selecionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um pedido na lista.")
            return None
        item = self.tree.item(selected[0])
        return item['values'][0]
