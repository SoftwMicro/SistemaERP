import tkinter as tk
from tkinter import ttk, messagebox


import requests
import mysql.connector
from tkinter import ttk

# --- Modelo ---
class ProdutoModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="hmg",
            password="010101",
            database="homologacao"
        )

    def listar_produtos(self):
        query = '''
            SELECT Produtos.Id, Produtos.Nome, ProdutoDetalhes.Descricao, ProdutoDetalhes.Ativo, Estoques.QuantidadeAtual, Precos.ValorCusto
            FROM Produtos
            JOIN ProdutoDetalhes ON Produtos.DetalhesId = ProdutoDetalhes.Id
            JOIN Estoques ON Estoques.ProdutoId = Produtos.Id
            LEFT JOIN Precos ON Precos.ProdutoId = Produtos.Id
        '''
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def close(self):
        self.conn.close()

# --- Controlador e View ---
class ProdutoForm(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        if parent is None:
            self.pack(fill=tk.BOTH, expand=True)
            self.master.title("Cadastro de Produto Integrado SKU")
            self.master.geometry("700x500")
            self.master.resizable(False, False)
        self.model = ProdutoModel()
        self.create_widgets()
        if hasattr(self, 'tree'):
            self.atualizar_grid()

    def create_widgets(self):
        # SKU
        ttk.Label(self, text="SKU:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.sku_entry = ttk.Entry(self)
        self.sku_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Nome
        ttk.Label(self, text="Nome:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Descrição
        ttk.Label(self, text="Descrição:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Quantidade em Estoque
        ttk.Label(self, text="Quantidade em Estoque:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.stock_entry = ttk.Entry(self)
        self.stock_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Ativo
        self.is_active_var = tk.BooleanVar(value=True)
        self.active_check = ttk.Checkbutton(self, text="Ativo", variable=self.is_active_var)
        self.active_check.grid(row=5, column=1, padx=10, pady=10, sticky="w")


        # Botão Salvar
        self.save_btn = ttk.Button(self, text="Salvar", command=self.on_save)
        self.save_btn.grid(row=6, column=0, columnspan=2, pady=20)

        # Grid de produtos
        columns = ("Id", "Nome", "Descricao", "Ativo", "QuantidadeAtual", "Preco")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        col_titles = ["Id", "Nome", "Descricao", "Ativo", "QuantidadeAtual", "Preço"]
        for col, title in zip(columns, col_titles):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=120)
        self.tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Ajuste de colunas
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # Preço
        ttk.Label(self, text="Preço:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(self, textvariable=self.price_var)
        self.price_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.price_entry.bind('<FocusOut>', self.formatar_moeda_event)
        
    def formatar_moeda_event(self, event=None):
        valor = self.price_var.get().strip()
        if not valor:
            self.price_var.set('')
            return
        valor = valor.replace('R$', '').replace(' ', '').replace(',', '.')
        try:
            valor_float = float(valor)
            valor_formatado = f'R$ {valor_float:,.2f}'
            valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
            self.price_var.set(valor_formatado)
        except ValueError:
            self.price_var.set('')



    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item['values']
        # Preencher campos
        self.sku_entry.delete(0, tk.END)
        self.sku_entry.insert(0, values[0])  # SKU recebe Id
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, values[2])
        # Preço recebe Preco
        self.price_entry.delete(0, tk.END)
        preco = values[5]
        if preco is not None and preco != "":
            # Se já está formatado, remove R$ e converte
            try:
                preco_float = float(str(preco).replace("R$", "").replace(",", ".").strip())
                self.price_entry.insert(0, f"R$ {preco_float:.2f}")
            except Exception:
                self.price_entry.insert(0, str(preco))
        else:
            self.price_entry.insert(0, "")
        # Quantidade em estoque recebe QuantidadeAtual como inteiro
        self.stock_entry.delete(0, tk.END)
        try:
            quantidade = int(float(values[4]))
            self.stock_entry.insert(0, str(quantidade))
        except Exception:
            self.stock_entry.insert(0, str(values[4]))
        # Ativo
        self.is_active_var.set(bool(values[3]))

    def on_save(self):
        API_BASE = "http://localhost:8000/api/v1"
        # Preço formatado para moeda na interface, decimal ao salvar
        preco_str = self.price_entry.get().replace("R$", "").replace(",", ".").strip()
        try:
            price = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido.")
            return
        try:
            stock_quantity = int(self.stock_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade em Estoque deve ser um número inteiro.")
            return
        dados = {
            "sku": self.sku_entry.get(),
            "name": self.name_entry.get(),
            "description": self.description_entry.get(),
            "price": price,
            "stock_quantity": stock_quantity,
            "is_active": self.is_active_var.get()
        }
        try:
            resp = requests.post(f"{API_BASE}/products", json=dados)
            if resp.status_code in (200, 201):
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                self.atualizar_grid()
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar produto.\nStatus: {resp.status_code}\nResposta: {resp.text}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro de conexão: {str(e)}")

    def atualizar_grid(self):
        # Limpa grid
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Busca dados do banco
        try:
            produtos = self.model.listar_produtos()
            for row in produtos:
                row_list = list(row)
                # Formatar QuantidadeAtual (índice 4) para inteiro
                if row_list[4] is not None:
                    try:
                        row_list[4] = str(int(float(row_list[4])))
                    except Exception:
                        row_list[4] = str(row_list[4])
                else:
                    row_list[4] = ""
                # Formatar preço para moeda na grid
                if row_list[5] is not None:
                    row_list[5] = f"R$ {float(row_list[5]):.2f}"
                else:
                    row_list[5] = ""
                self.tree.insert("", "end", values=row_list)
        except Exception as e:
            messagebox.showerror("Erro ao carregar produtos", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProdutoForm(root)
    root.mainloop()
