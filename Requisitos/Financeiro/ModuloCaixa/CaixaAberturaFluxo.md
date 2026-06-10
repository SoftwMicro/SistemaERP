┌─────────────────────┐
│  TelaInicial (UI)   │
│  ├─ Carrega dados   │
│  └─ Exibe grid      │
└──────────┬──────────┘
           │
     ┌─────▼──────────┐
     │   Repository   │
     │   (API Layer)  │
     └─────┬──────────┘
           │
     ┌─────▼──────────┐
     │  Backend API   │
     │  /caixa/...    │
     └────────────────┘