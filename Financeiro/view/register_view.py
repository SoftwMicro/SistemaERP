import tkinter as tk
from tkinter import messagebox, ttk


class RegisterView:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Cadastro de Usuário")
        self.window.resizable(False, False)
        self.window.grab_set()
        self._build_form()

    def _build_form(self) -> None:
        frame = ttk.Frame(self.window, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
        self.nome_entry = ttk.Entry(frame, width=34)
        self.nome_entry.grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Login:").grid(row=1, column=0, sticky="w", pady=4)
        self.login_entry = ttk.Entry(frame, width=34)
        self.login_entry.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky="w", pady=4)
        self.senha_entry = ttk.Entry(frame, width=34, show="*")
        self.senha_entry.grid(row=2, column=1, pady=4)

        ttk.Label(frame, text="Perfil:").grid(row=3, column=0, sticky="w", pady=4)
        self.perfil_combo = ttk.Combobox(
            frame,
            values=["Caixa", "Gerente", "Admin"],
            state="readonly",
            width=32,
        )
        self.perfil_combo.grid(row=3, column=1, pady=4)
        self.perfil_combo.current(0)

        self.ativo_var = tk.BooleanVar(value=True)
        self.ativo_check = ttk.Checkbutton(
            frame, text="Ativo", variable=self.ativo_var
        )
        self.ativo_check.grid(row=4, column=1, sticky="w", pady=4)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=12)

        ttk.Button(button_frame, text="Salvar", command=self._on_save).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(button_frame, text="Cancelar", command=self.window.destroy).grid(
            row=0, column=1, padx=6
        )

    def _on_save(self) -> None:
        try:
            usuario = self.controller.register_user(
                nome=self.nome_entry.get(),
                login=self.login_entry.get(),
                senha=self.senha_entry.get(),
                perfil=self.perfil_combo.get(),
                ativo=self.ativo_var.get(),
            )
            messagebox.showinfo(
                "Sucesso",
                f"Usuário '{usuario.login}' cadastrado com sucesso.",
                parent=self.window,
            )
            self.window.destroy()
        except ValueError as error:
            messagebox.showerror("Erro de validação", str(error), parent=self.window)
        except Exception as error:
            messagebox.showerror("Erro", str(error), parent=self.window)
