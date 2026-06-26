import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from ..controller.comprovante_controller import ComprovanteController
from ..utils.currency import format_brazilian_currency


class EmitirComprovanteView:
    def __init__(self, owner):
        self.owner = owner
        parent = getattr(owner, "root", owner)
        self.controller = ComprovanteController()
        self.window = tk.Toplevel(parent)
        self.window.title("Emitir Comprovante")
        self.window.geometry("900x700")
        self.window.minsize(900, 700)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grab_set()
        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.window, padding=12)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        search_frame = ttk.LabelFrame(main_frame, text="Dados do Comprovante", padding=10)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="ID do Pedido:").grid(row=0, column=0, sticky="w", pady=4)
        self.pedido_entry = ttk.Entry(search_frame, width=28)
        self.pedido_entry.grid(row=0, column=1, sticky="w", pady=4)
        self.pedido_entry.focus()

        ttk.Label(search_frame, text="Tipo de Comprovante:").grid(row=1, column=0, sticky="w", pady=4)
        self.tipo_combobox = ttk.Combobox(
            search_frame,
            values=["Fiscal", "Não Fiscal"],
            state="readonly",
            width=26,
        )
        self.tipo_combobox.grid(row=1, column=1, sticky="w", pady=4)

        ttk.Label(search_frame, text="Número do Comprovante (opcional):").grid(row=2, column=0, sticky="w", pady=4)
        self.numero_entry = ttk.Entry(search_frame, width=28)
        self.numero_entry.grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(search_frame, text="Data de Emissão (opcional):").grid(row=3, column=0, sticky="w", pady=4)
        self.data_emissao_entry = ttk.Entry(search_frame, width=28)
        self.data_emissao_entry.grid(row=3, column=1, sticky="w", pady=4)
        self.data_emissao_entry.insert(0, "YYYY-MM-DDTHH:MM:SS")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.emit_button = ttk.Button(button_frame, text="Emitir Comprovante", command=self._on_emit)
        self.emit_button.grid(row=0, column=0, padx=4)
        ttk.Button(button_frame, text="Fechar", command=self.window.destroy).grid(row=0, column=1, padx=4)

        self.feedback_label = ttk.Label(main_frame, text="", wraplength=860, justify="left", foreground="black")
        self.feedback_label.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        receipt_frame = ttk.LabelFrame(main_frame, text="Comprovante", padding=10)
        receipt_frame.grid(row=3, column=0, sticky="nsew")
        receipt_frame.grid_rowconfigure(0, weight=1)
        receipt_frame.grid_columnconfigure(0, weight=1)

        self.receipt_text = tk.Text(
            receipt_frame,
            wrap="none",
            font=("Courier", 10),
            state="disabled",
        )
        self.receipt_text.grid(row=0, column=0, sticky="nsew")

        text_scroll = ttk.Scrollbar(receipt_frame, orient="vertical", command=self.receipt_text.yview)
        self.receipt_text.configure(yscrollcommand=text_scroll.set)
        text_scroll.grid(row=0, column=1, sticky="ns")

    def _on_emit(self) -> None:
        pedido_id_text = self.pedido_entry.get().strip()
        if not pedido_id_text:
            self._show_feedback("Informe o ID do pedido.", color="red")
            return

        try:
            pedido_id = int(pedido_id_text)
        except ValueError:
            self._show_feedback("ID do pedido deve ser um número inteiro.", color="red")
            return

        tipo = self.tipo_combobox.get().strip()
        if not tipo:
            self._show_feedback("Selecione o tipo de comprovante.", color="red")
            return

        numero = self.numero_entry.get().strip() or None
        data_emissao = self.data_emissao_entry.get().strip() or None
        if data_emissao and not self._validar_iso_datetime(data_emissao):
            self._show_feedback(
                "Data de emissão deve estar no formato ISO 8601: YYYY-MM-DDTHH:MM:SS.",
                color="red",
            )
            return

        self._set_action_buttons_state("disabled")
        self._clear_feedback()

        try:
            response = self.controller.emitir_comprovante(
                pedido_id=pedido_id,
                tipo=tipo,
                numero_comprovante=numero,
                data_emissao=data_emissao,
            )
            self._show_feedback("Comprovante emitido com sucesso.", color="green")
            self._show_receipt(response)
        except ValueError as error:
            self._show_feedback(str(error), color="red")
        except ConnectionError as error:
            self._show_feedback(str(error), color="red")
        except Exception as error:
            self._show_feedback(f"Erro inesperado ao emitir comprovante: {error}", color="red")
        finally:
            self._set_action_buttons_state("normal")

    def _show_receipt(self, data: dict) -> None:
        content = self._build_receipt_text(data)
        self.receipt_text.configure(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, content)
        self.receipt_text.configure(state="disabled")

    def _build_receipt_text(self, data: dict) -> str:
        receipt = data.get("receipt", {})
        rows = data.get("rows", [])
        linha = "=" * 60
        separator = "-" * 60
        lines = [
            linha,
            "                      NOME DA EMPRESA                       ",
            "                 CNPJ: 00.000.000/0001-00                   ",
            "             Rua dos Desenvolvedores, 1024 - TI            ",
            linha,
            f"              EXTRATO No. {receipt.get('orderId', '—')}",
            f"                  CUPOM FISCAL ELETRÔNICO                    ",
            linha,
            f"Comprovante: {receipt.get('numeroComprovante', '—')}",
            f"Tipo: {receipt.get('tipo', '—')}",
            f"Data de Emissão: {self._format_datetime(receipt.get('dataEmissao'))}",
            separator,
            "# | COD | DESCRIÇÃO | QTD | UN | VL UN R$ | VL ITEM R$",
            separator,
        ]

        for index, row in enumerate(rows, start=1):
            product_line = f"{index} | {row.get('sku', '—')} | {row.get('nomeProduto', '—')}"
            qty = row.get('quantidade', '—')
            unit_price = self._format_currency(row.get('precoUnitario'))
            subtotal = self._format_currency(row.get('subtotal'))
            lines.append(product_line)
            lines.append(
                f"               {qty} UN X {unit_price} -> R$ {subtotal}"
            )
            lines.append(separator)

        total_geral = self._format_currency(data.get('totalGeral') or receipt.get('totalGeral') or self._calculate_total(rows))
        valor_pago = self._format_currency(rows[0].get('valorPago')) if rows else "R$ 0,00"
        forma_pagamento = rows[0].get('formaPagamento', '—') if rows else '—'
        status_pagamento = rows[0].get('statusPagamento', '—') if rows else receipt.get('statusPagamento', '—')

        lines.extend([
            f"TOTAL BRUTO R$                                     {total_geral}",
            separator,
            "FORMA DE PAGAMENTO                                 VALOR PAGO R$",
            f"{forma_pagamento}                                  {valor_pago}",
            separator,
            f"Status do Pagamento: {status_pagamento}",
            linha,
            "          OBRIGADO PELA PREFERENCIA - VOLTE SEMPRE          ",
            linha,
        ])

        return "\n".join(lines)

    def _calculate_total(self, rows: list[dict]) -> float:
        total = 0.0
        for row in rows:
            try:
                total += float(str(row.get("subtotal", 0)).replace(",", "."))
            except (TypeError, ValueError):
                continue
        return total

    def _format_datetime(self, value: str | None) -> str:
        if not value:
            return "—"

        if isinstance(value, datetime.datetime):
            dt = value
        else:
            try:
                dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return str(value)

        return dt.strftime("%d/%m/%Y %H:%M")

    def _format_currency(self, value: float | int | str | None) -> str:
        try:
            if value is None or value == "":
                return "R$ 0,00"
            return format_brazilian_currency(float(str(value).replace("R$", "").replace(" ", "").replace(",", ".")))
        except (TypeError, ValueError):
            return str(value)

    def _validar_iso_datetime(self, text: str) -> bool:
        try:
            datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False

    def _set_action_buttons_state(self, state: str) -> None:
        self.emit_button.configure(state=state)

    def _show_feedback(self, message: str, color: str = "black") -> None:
        self.feedback_label.configure(text=message, foreground=color)

    def _clear_feedback(self) -> None:
        self.feedback_label.configure(text="", foreground="black")
