def format_brazilian_currency(value: float) -> str:
    """Formata um valor numérico como moeda brasileira."""
    if value is None:
        return "R$ 0,00"

    formatted = f"{value:,.2f}"
    return f"R$ {formatted.replace(',', 'X').replace('.', ',').replace('X', '.') }"
