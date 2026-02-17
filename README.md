#Babylon_finances 💰

A personal finance app developed in **Python**, designed to help you record income, expenses, savings, and perform basic financial analysis locally and securely.

---

## 📌 Main Features

- Recording of **income** and **expenses**
- Expense categorization (food, leisure, transportation, etc.)
- Basic financial analysis
- **Local** data storage (no personal data is uploaded to GitHub)
- "Financial app based on 'The Richest Man in Babylon'. Evolved from CLI → EXE → FastAPI."

- Project intended for personal use and hands-on learning.

---

## 🛠️ Technologies Used

- Python 3
- .EXE
- Fast API
- JSON (local storage)
- Git and GitHub

---

## 📂 Project Structure

```text
BABILONIA_FINANZAS/
│
├── app/                                         # 🚀 Arranque de la aplicación
│   ├── main.py                                  # FastAPI app, middlewares, routers
│   │
│   └── core/                                    # Cross-cutting concerns
│       ├── __init__.py
│       ├── config.py                            # Settings, env
│       ├── logging.py                           # Logging estructurado
│       └── exceptions.py                        # Mapeo errores dominio → HTTP
│
├── api/                                         # 🌐 Capa HTTP (FastAPI)
│   └── v1/
│       ├── __init__.py
│       ├── deps.py                              # 🔥 INYECCIÓN CENTRALIZADA
│       │
│       ├── routes/                              # Endpoints
│       │   ├── __init__.py
│       │   ├── income.py
│       │   ├── dashboard.py
│       │   ├── auth.py
│       │   ├── expenses.py
│       │   ├── balance.py
│       │   └── reports.py
│       │
│       └── schemas/                             # Contratos HTTP
│           ├── __init__.py
│           ├── income.py
│           ├── auth.py
│           ├── expense.py
│           ├── report.py
│           └── common.py
│ 
├── legacy/                                      # ⚠️ Código heredado (temporal)
│   ├── __init__.py
│   └── finance_logic.py
│
├── domain/                                      # ❤️ CORAZÓN DEL NEGOCIO
│   ├── __init__.py
│   │
│   ├── exceptions.py
│   │
│   ├── entities/                                # Entidades del dominio
│   │   ├── __init__.py
│   │   ├── income.py
│   │   ├── expense.py
│   │   └── category.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── finance_repository.py                # Interfaz abstracta
│   │
│   ├── services/                                # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── debt_policy.py
│   │   ├── balance_service.py
│   │   ├── finance_logic.py
│   │   ├── babylonian_rules.py
│   │   └── report_service.py
│   │
│   └── ports/                                  # Interfaces (contratos)
│       └── __init__.py
│              ├── debt_policy.py
│	       └── finance_repository.py
│
├── infrastructure/                             # 🔌 Detalles técnicos
│   ├── __init__.py
│   │
│   ├── db/                                     # Bases de datos
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── sqlite.py
│   │   └── postgres.py
│   │
│   ├── repositories/                           # Implementaciones reales
│   │   ├── __init__.py
│   │   ├── json_finance_repository.py
│   │   ├── fake_finance_repository.py           # Implementación
│   │   ├── report_repository.py
│   │   └── in_memory.py                         # Repo real usado por FastAPI
│   │
│   ├── storage/                                 # Archivos / exports
│   │   ├── __init__.py
│   │   ├── storage.py
│   │   └── data/
│   │       └── datos.json
│   │
│   ├── security/                                # Seguridad técnica
│   │   ├── __init__.py
│   │   ├── encryption.py
│   │   ├── hashing.py
│   │   ├── jwt.py
│   │   └── rate_limit.py
│   │
│   └── config/                                  # Config infra
│       ├── __init__.py
│       └── settings.py
│
├──application/ 
│   ├── __init__.py 
│   ├── use_cases/ 
│   │    ├── __init__.py 
│   │    ├── register_income.py 
│   │    ├── register_expense.py 
│   │    ├── get_balance.py 
│   │    └── generate_report.py 
│   │ 
│   └── dto/ 
│         ├── __init__.py 
│         ├── income_dto.py 
│         └── expense_dto.py
│
│
├── i18n/   
│   ├── __init__.py                           # 🌍 Idiomas (UX)
│   ├── quotes.py
│   ├── es.py
│   ├── en.py
│   └── lang.py
│
├── reports_output/                           # 📊 Archivos generados
│   ├── reports/
│   ├── ahorro_babilonico_2026-01.txt
│   ├── evolucion_financiera.png
│   └── evolucion_financiera_2026-01.txt
│
├── cli/                                      # 🖥️ CLI
│   ├── __init__.py
│   └── menu.py
│
├── scripts/                                  # Utilidades
│   ├── __init__.py                  
│   ├── migrate_categories.py
│   ├── search_word.py
│   └── example_data.json
│
├── tests/ 
│    ├── __init__.py                         👈 NUEVO (solo esto), # 🧪 Tests
│    │           
│    ├── conftest.py                         # 🔧 Fixtures compartidos (pytest)
│    │                
│    ├── unit/                               # 🧠 Tests PUROS (rápidos)
│    │    ├── __init__.py 
│    │    │                 
│    │    ├── domain/                        # ❤️ Dominio (sin FastAPI)
│    │    │    ├── __init__.py 
│    │    │    ├── test_income.py
│    │    │    ├── test_expense.py
│    │    │    ├── test_category.py
│    │    │    └── test_babylonian_rules.py
│    │    │      
│    │    └── application/                   # 🎯 UseCases
│    │         ├── __init__.py
│    │         ├── test_register_income.py
│    │         ├── test_register_expense.py
│    │         └── test_get_balance.py
│    │
│    └── integration/                        # 🌐 Tests de API (FastAPI real)
│         ├── __init__.py
│         ├── test_income_api.py
│         ├── test_expense_api.py
│         ├── test_expense_api.py
│         ├── test_balance_api.py
│         └── test_auth_api.py
│
├── pytest.ini
│
├── .env
├── .gitignore
├── FinanzasDeBabilonia.spec                 # PyInstaller
└── README.md


---

## 📈 Project Status

🟡 In Development

Project created as part of hands-on learning in Python and GitHub.

---

## 👤 Author

Pedro Nicanor Betancourt Achagua
Personal Project – Finance & Programming

---

## 📄 License

Personal and educational use.







