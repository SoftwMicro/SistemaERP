import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import importlib

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema ERP")
        self.state('zoomed')  # Maximiza a janela
        self.create_menu()
        self.current_window = None
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        menubar = tk.Menu(self)

        # Menu Cadastro
        cadastro_menu = tk.Menu(menubar, tearoff=0)
        cadastro_menu.add_command(label="Cliente", command=self.abrir_cliente)
        cadastro_menu.add_command(label="Produto", command=self.abrir_produto)
        menubar.add_cascade(label="Cadastro", menu=cadastro_menu)

        # Menu Gerenciar Pedidos
        pedidos_menu = tk.Menu(menubar, tearoff=0)
        pedidos_menu.add_command(label="Solicitar Pedido", command=self.abrir_solicitar_pedido)
        pedidos_menu.add_command(label="Pedidos", command=self.abrir_listar_pedidos)
        menubar.add_cascade(label="Gerenciar Pedidos", menu=pedidos_menu)

        self.config(menu=menubar)

    def limpar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def abrir_cliente(self):
        self.limpar_main_frame()
        modulo = importlib.import_module("cliente_form")
        form = modulo.ClienteForm(self.main_frame)
        form.pack(fill=tk.BOTH, expand=True)

    def abrir_produto(self):
        self.limpar_main_frame()
        modulo = importlib.import_module("produto_form")
        form = modulo.ProdutoForm(self.main_frame)
        form.pack(fill=tk.BOTH, expand=True)

    def abrir_solicitar_pedido(self):
        self.limpar_main_frame()
        modulo = importlib.import_module("order_form")
        form = modulo.PedidoForm(self.main_frame)
        form.pack(fill=tk.BOTH, expand=True)

    def abrir_listar_pedidos(self):
        self.limpar_main_frame()
        modulo = importlib.import_module("order_form_list")
        form = modulo.OrderListForm(self.main_frame)
        form.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
