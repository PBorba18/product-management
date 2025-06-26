# Product Management Fullstack

Sistema completo de gerenciamento de produtos, com cadastro, listagem, descontos (percentual ou via cupom), frontend moderno com React + TypeScript e backend robusto em Flask + SQLAlchemy.

---

## **Competências demonstradas neste projeto**

- **Frontend moderno:**  
  - React 18 + Vite + TypeScript  
  - Componentização e organização em pastas (services, components, pages, models)
  - Consumo de API RESTful (CRUD completo)
  - Utilização de modais, validação de formulários e feedback visual com Toasts
  - Estilização responsiva (Tailwind CSS)
  - Gerenciamento de estado com hooks React

- **Backend robusto:**  
  - Flask + Flask-RESTX (API RESTful documentada via Swagger)
  - SQLAlchemy (ORM) + SQLite para persistência de dados
  - CORS configurado para múltiplas portas (facilitando integração local)
  - Padrão Factory de inicialização (create_app)
  - Blueprint/Namespace para organização de rotas
  - Validação, paginação, filtros, lógica de desconto e aplicação de cupons
  - Migrations com Flask-Migrate

- **Integração Fullstack:**  
  - Comunicação assíncrona via HTTP (axios/fetch)
  - Tratamento de erros, exibição de feedback ao usuário, reload dinâmico de dados

---

## **Requisitos de sistema**

- **Backend:**
  - Python 3.10+
  - Pipenv ou virtualenv (recomendado)
  - Flask, Flask-RESTX, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS

- **Frontend:**
  - Node.js 18+
  - npm ou yarn
  - Vite, React, TypeScript, Tailwind CSS, axios, react-toastify

---

## **Como rodar o projeto**

### **1. Clonar o repositório**

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
2. Rodando o Backend (Flask)
bash
Copiar
Editar
cd backend
# Crie e ative o ambiente virtual
python -m venv venv
# Ativar: (Windows)
venv\Scripts\activate
# Ativar: (Linux/Mac)
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações e o servidor
flask db upgrade
python run.py
O backend estará disponível em:
http://localhost:5000/api/products/

Documentação Swagger:
http://localhost:5000/api/docs/

3. Rodando o Frontend (React + Vite)
bash
Copiar
Editar
cd my-app
npm install
npm run dev
O frontend estará disponível em:
http://localhost:5173/produtos

URLs de acesso rápido
Frontend:
http://localhost:5173/produtos

API Backend:
http://localhost:5000/api/products/

Documentação Swagger (API):
http://localhost:5000/api/docs/

Funcionalidades
Cadastro, edição e exclusão de produtos

Listagem paginada com busca, filtro, ordenação

Aplicação de cupons e descontos percentuais

Modais para criar e editar produtos, aplicar descontos

Feedback visual em todas as operações

Proteção de CORS para integração local

Screenshots
Adicione aqui prints das telas principais do sistema para ilustrar.

Dicas
Banco:
O projeto usa SQLite por padrão para facilitar testes locais.

Migrações:
Caso altere modelos, use flask db migrate && flask db upgrade.

Ambiente:
Sempre ative o virtualenv antes de rodar o backend.

Autor e Licença
Projeto desenvolvido por Paulo Messias dos santos Borba
Fique à vontade para utilizar como base de estudos ou adaptar em outros sistemas.