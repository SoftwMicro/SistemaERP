import tkinter as tk
import os, sys
from tkinter import ttk, messagebox
from .cliente_view import ClienteView
from .produto_view import ProdutoView
from .pedido_view import PedidoView
from views.vendas.vendas_view import VendasView

class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("POS - Sistema de Vendas")
        self.root.geometry("900x600")
        # Caminho do ícone para PyInstaller e execução normal
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'app.ico')
        else:
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.ico'))
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            pass  # Se não conseguir definir o ícone, ignora
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)
        self.cliente_tab = ttk.Frame(tab_control)
        self.produto_tab = ttk.Frame(tab_control)
        self.pedido_tab = ttk.Frame(tab_control)
        self.vendas_tab = ttk.Frame(tab_control)

        tab_control.add(self.cliente_tab, text='Clientes')
        tab_control.add(self.produto_tab, text='Produtos')
        tab_control.add(self.pedido_tab, text='Pedidos')
        tab_control.add(self.vendas_tab, text='Vendas')
        tab_control.pack(expand=1, fill='both')

        self.cliente_view = ClienteView(self.cliente_tab)
        self.produto_view = ProdutoView(self.produto_tab)
        self.pedido_view = PedidoView(self.pedido_tab)
        self.vendas_view = VendasView(self.vendas_tab)

    def run(self):
        self.root.mainloop()
