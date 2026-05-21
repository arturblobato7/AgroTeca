# 🌱 AgroTeca — Biblioteca Comunitária de Jutaiteua

A AgroTeca é uma plataforma digital comunitária desenvolvida para preservar, organizar e compartilhar conhecimentos agrícolas, culturais e educativos da comunidade de Jutaiteua, no interior do Pará.

O sistema conecta tecnologia e saberes tradicionais amazônicos, permitindo que moradores enviem conteúdos que passam por um processo de curadoria antes da publicação.

---

# 🌎 Objetivo do Projeto

Fortalecer a agricultura familiar e valorizar os conhecimentos tradicionais da comunidade através de uma plataforma acessível, colaborativa e sustentável.

---

# 🚀 Funcionalidades Implementadas

## 📚 Biblioteca Comunitária
- Página inicial institucional
- Informações sobre a comunidade
- Técnicas de plantio
- Cartilhas comunitárias
- Vídeos educativos
- Página de conteúdos aprovados

---

## 🛡️ Sistema de Curadoria
- Envio de conteúdos pela comunidade
- Aprovação de conteúdos
- Rejeição de conteúdos
- Exclusão de conteúdos
- Edição de conteúdos enviados
- Painel administrativo protegido por login

---

## 📈 Sistema Dinâmico de Preços Agrícolas
- Cadastro de preços agrícolas
- Atualização dinâmica via banco de dados
- Tendência automática:
  - 📈 Subiu
  - 📉 Caiu
  - ➖ Estável
- Exclusão de preços
- Edição de preços
- Página pública atualizada automaticamente

---

# 🧠 Tecnologias Utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2
- Git
- GitHub

---

# 📂 Estrutura do Projeto

```bash
AGROTECA/
│
├── app.py
├── db.py
├── database.db
├── .gitignore
├── README.md
│
├── static/
│   ├── style.css
│   ├── index.css
│   ├── preco.css
│   ├── tecnicas.css
│   └── videos.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comunidade.html
│   ├── tecnicas.html
│   ├── cartilhas.html
│   ├── videos.html
│   ├── enviar.html
│   ├── conteudos.html
│   ├── admin.html
│   ├── admin_precos.html
│   ├── editar_conteudo.html
│   ├── editar_preco.html
│   ├── login.html
│   └── precos.html
│
└── __pycache__/
```

---

# ⚙️ Como Executar o Projeto

## 1️⃣ Clone o repositório

```bash
git clone LINK_DO_REPOSITORIO
```

---

## 2️⃣ Entre na pasta

```bash
cd AGROTECA
```

---

## 3️⃣ Instale o Flask

```bash
pip install flask
```

---

## 4️⃣ Execute o projeto

```bash
python app.py
```

---

## 5️⃣ Acesse no navegador

```txt
http://127.0.0.1:5000
```

---

# 🔐 Login Administrativo

```txt
Usuário: curador
Senha: 1234
```

---

# 🧩 Funcionalidades Técnicas

## CRUD de Conteúdos
- Create → Enviar conteúdo
- Read → Visualizar conteúdos
- Update → Editar conteúdo
- Delete → Excluir conteúdo

---

## CRUD de Preços
- Create → Cadastrar preço
- Read → Exibir preços
- Update → Editar preço
- Delete → Excluir preço

---

# 🎨 Interface

A interface foi desenvolvida com foco em:
- simplicidade;
- acessibilidade;
- identidade amazônica;
- experiência comunitária.

---

# 🌱 Impacto Social

A AgroTeca busca:
- preservar conhecimentos tradicionais;
- incentivar agricultura familiar;
- democratizar acesso à informação;
- fortalecer comunidades rurais;
- integrar tecnologia e cultura amazônica.

---

# 🚧 Próximas Implementações

- Upload real de imagens
- Upload de PDFs
- Upload de vídeos
- Sistema de usuários
- Busca de conteúdos
- Filtros por categoria
- Comentários da comunidade
- Integração com APIs agrícolas
- Dashboard estatístico
- Deploy online
- Responsividade mobile avançada

---

# 👨‍💻 Desenvolvimento

Projeto acadêmico desenvolvido para o Amazon Hacking, com foco em tecnologia social, sustentabilidade e valorização cultural amazônica.
