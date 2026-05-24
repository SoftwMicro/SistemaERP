import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

# --- Modelos ---
class ClienteModel:
    def __init__(self, id, nome, cpf_cnpj, email, telefone, endereco):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

class ProdutoModel:
    def __init__(self, id, sku, nome, descricao, preco, quantidade_estoque, ativo):
        self.id = id
        self.sku = sku
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.ativo = ativo

# --- Controller ---
class PedidoController:
    @staticmethod
    def buscar_cliente_por_id(cliente_id):
        resp = requests.get(f"{API_BASE}/customers/{cliente_id}")
        if resp.status_code == 200:
            c = resp.json()
            return ClienteModel(c["id"], c["nome"], c["cpf_cnpj"], c["email"], c["telefone"], c["endereco"])
        return None

    @staticmethod
    def listar_produtos():
        resp = requests.get(f"{API_BASE}/products")
        produtos = []
        if resp.status_code == 200:
            for p in resp.json():
                produtos.append(ProdutoModel(
                    p.get("id"),
                    p.get("sku"),
                    p.get("name", p.get("nome", "")),
                    p.get("description", p.get("descricao", "")),
                    p.get("price", p.get("preco", 0)),
                    p.get("stock_quantity", p.get("quantidade_estoque", 0)),
                    p.get("is_active", p.get("ativo", True))
                ))
        return produtos

    @staticmethod
    def solicitar_pedido(cliente_id, itens, observacoes=""):
        payload = {
            "cliente": cliente_id,
            "itens": itens,
            "observacoes": observacoes
        }
        resp = requests.post(f"{API_BASE}/orders", json=payload)
        return resp

# --- View ---
class PedidoForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solicitar Pedido")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.selected_cliente = None
        self.produtos = []
        self.create_widgets()
        self.carregar_produtos()

    def create_widgets(self):
        # Pesquisa Cliente
        ttk.Label(self, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cliente_id_entry = ttk.Entry(self, width=10)
        self.cliente_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.pesquisar_btn = ttk.Button(self, text="Pesquisar", command=self.pesquisar_cliente)
        self.pesquisar_btn.grid(row=0, column=2, padx=5, pady=5)

        # Grid Cliente
        self.cliente_tree = ttk.Treeview(self, columns=("id", "nome", "cpf_cnpj", "email", "telefone", "endereco"), show="headings", height=2)
        for col in ("id", "nome", "cpf_cnpj", "email", "telefone", "endereco"):
            self.cliente_tree.heading(col, text=col.capitalize())
            self.cliente_tree.column(col, width=120)
        self.cliente_tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.cliente_tree.bind("<<TreeviewSelect>>", self.on_cliente_select)

        # Grid Produtos
        ttk.Label(self, text="Produtos Disponíveis:").grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.produto_tree = ttk.Treeview(self, columns=("id", "sku", "nome", "descricao", "preco", "quantidade_estoque", "ativo"), show="headings", selectmode="extended", height=10)
        col_titles = ["ID", "SKU", "Nome", "Descrição", "Preço", "Qtd. Estoque", "Ativo"]
        for col, title in zip(("id", "sku", "nome", "descricao", "preco", "quantidade_estoque", "ativo"), col_titles):
            self.produto_tree.heading(col, text=title)
            self.produto_tree.column(col, width=100)
        self.produto_tree.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Observações
        ttk.Label(self, text="Observações:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.obs_entry = ttk.Entry(self, width=80)
        self.obs_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Botão Realizar Pedido
        self.pedido_btn = ttk.Button(self, text="Realizar Pedido", command=self.realizar_pedido)
        self.pedido_btn.grid(row=5, column=3, padx=5, pady=20, sticky="e")
        self.pedido_btn.config(state=tk.NORMAL)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def pesquisar_cliente(self):
        cid = self.cliente_id_entry.get().strip()
        if not cid.isdigit():
            messagebox.showerror("Erro", "Informe um ID de cliente válido.")
            return
        cliente = PedidoController.buscar_cliente_por_id(cid)
        for item in self.cliente_tree.get_children():
            self.cliente_tree.delete(item)
        if cliente:
            self.cliente_tree.insert("", "end", values=(cliente.id, cliente.nome, cliente.cpf_cnpj, cliente.email, cliente.telefone, cliente.endereco))
            self.selected_cliente = cliente
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            self.selected_cliente = None

    def on_cliente_select(self, event):
        selected = self.cliente_tree.selection()
        if selected:
            item = self.cliente_tree.item(selected[0])
            values = item['values']
            self.selected_cliente = ClienteModel(*values)

    def carregar_produtos(self):
        self.produtos = PedidoController.listar_produtos()
        for item in self.produto_tree.get_children():
            self.produto_tree.delete(item)
        for prod in self.produtos:
            self.produto_tree.insert("", "end", values=(prod.id, prod.sku, prod.nome, prod.descricao, f"R$ {float(prod.preco):.2f}", prod.quantidade_estoque, "Sim" if prod.ativo else "Não"))

    def realizar_pedido(self):
        self.pedido_btn.config(state=tk.DISABLED, text="Enviando...")
        self.update_idletasks()
        # Cliente selecionado
        selected_cliente = self.selected_cliente
        if not selected_cliente:
            messagebox.showerror("Erro", "Selecione um cliente para o pedido.")
            self.pedido_btn.config(state=tk.NORMAL, text="Realizar Pedido")
            return
        # Produtos selecionados
        selected_items = self.produto_tree.selection()
        if not selected_items:
            messagebox.showerror("Erro", "Selecione ao menos um produto.")
            self.pedido_btn.config(state=tk.NORMAL, text="Realizar Pedido")
            return
        itens = []
        for item in selected_items:
            values = self.produto_tree.item(item)['values']
            produto_id = values[0]  # id do produto
            quantidade = 1  # Padrão 1, pode ser expandido para input de quantidade
            itens.append({"produto": produto_id, "quantidade": quantidade})
        observacoes = self.obs_entry.get().strip()
       
        payload = {
            "cliente_id": selected_cliente.id,
            "itens": itens,
            "observacoes": observacoes
        }
        print("JSON enviado para /orders:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        try:
            # Enviar o payload corretamente como JSON
            resp = requests.post(f"{API_BASE}/orders", json=payload)
            if resp.status_code in (200, 201):
                messagebox.showinfo("Sucesso", "Pedido realizado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Erro ao realizar pedido.\nStatus: {resp.status_code}\nResposta: {resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")
        self.pedido_btn.config(state=tk.NORMAL, text="Realizar Pedido")

if __name__ == "__main__":
    app = PedidoForm()
    app.mainloop()
