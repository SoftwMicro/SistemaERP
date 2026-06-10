# Repository Layer - Camada de Acesso à API

## Objetivo
A camada de `repository` centraliza todas as chamadas HTTP para a API, separando a lógica de comunicação com o backend da interface gráfica (View).

## Padrão de Arquitetura
```
View (UI) 
    ↓
Repository (API Calls)
    ↓
Backend API
```

## Benefícios
- **Separação de responsabilidades**: A View não conhece detalhes da API
- **Reutilização de código**: Repositorys podem ser usados por múltiplas Views
- **Facilidade de teste**: APIs podem ser mockadas nos testes
- **Manutenção centralizada**: Alterações na API ficam em um único lugar

## Exemplo de Uso

### Em uma View:
```python
from ..repository.caixa_repository import CaixaRepository

class MinhaView:
    def __init__(self):
        self.repository = CaixaRepository()
    
    def executar_acao(self):
        # Chamada centralizada
        resultado = self.repository.obter_aberturas(usuario_id=1)
```

## Estrutura Atual

### `caixa_repository.py`
Gerencia chamadas relacionadas a operações de caixa:
- `abrir_caixa(usuario_id, saldo_inicial)` - POST /caixa/abrir
- `obter_aberturas(usuario_id)` - GET /caixa/obter-abertura?usuarioId={id}

## Tratamento de Erros
O repository trata os seguintes cenários:
- ✅ **200 OK**: Retorna os dados processados
- ✅ **404 Not Found**: Retorna lista vazia (para obter_aberturas)
- ❌ **Outros erros HTTP**: Lança `ValueError`
- ❌ **Erros de conexão**: Lança `ConnectionError`
- ❌ **JSON inválido**: Lança `ValueError`

## Próximas Repositories a Implementar
- `user_repository.py` - Login, registro, autenticação
- `pagamento_repository.py` - Operações de pagamento
- `comprovante_repository.py` - Emissão de comprovantes
