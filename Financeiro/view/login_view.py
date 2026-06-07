import tkinter as tk
from tkinter import messagebox, ttk

from .register_view import RegisterView
from .telainicial import TelaInicial


class LoginView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Login - Sistema Financeiro")
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=18)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Acesso ao Sistema Financeiro", font=(None, 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 12)
        )

        ttk.Label(frame, text="Login:").grid(row=1, column=0, sticky="w", pady=4)
        self.login_entry = ttk.Entry(frame, width=36)
        self.login_entry.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky="w", pady=4)
        self.senha_entry = ttk.Entry(frame, width=36, show="*")
        self.senha_entry.grid(row=2, column=1, pady=4)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=12)

        ttk.Button(button_frame, text="Entrar", command=self._on_login).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(
            button_frame,
            text="Registrar novo usuário",
            command=self._open_register,
        ).grid(row=0, column=1, padx=6)

    def _on_login(self) -> None:
        login = self.login_entry.get().strip()
        senha = self.senha_entry.get().strip()
        try:
            usuario = self.controller.login(login, senha)
            messagebox.showinfo(
                "Bem-vindo",
                f"Usuário {usuario.nome} autenticado com sucesso!\nPerfil: {usuario.perfil}",
                parent=self.root,
            )
            self._open_main_screen(usuario)
        except PermissionError as error:
            messagebox.showwarning("Acesso negado", str(error), parent=self.root)
        except ValueError as error:
            messagebox.showerror("Falha na autenticação", str(error), parent=self.root)
        except Exception as error:
            messagebox.showerror("Erro", str(error), parent=self.root)

    def _open_register(self) -> None:
        RegisterView(self.controller, self.root)

    def _open_main_screen(self, usuario) -> None:
        self.root.withdraw()
        tela_inicial = TelaInicial(usuario)
        tela_inicial.run()

    def run(self) -> None:
        self.root.mainloop()
