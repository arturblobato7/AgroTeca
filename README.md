# 🌱 AgroTeca — Biblioteca Comunitária de Jutaiteua

A AgroTeca é uma plataforma digital comunitária criada para preservar, organizar e compartilhar conhecimentos agrícolas, culturais e educativos da comunidade de Jutaiteua, no interior do Pará.

O projeto busca conectar tecnologia e saberes tradicionais amazônicos, permitindo que moradores compartilhem conteúdos que passam por um processo de curadoria antes da publicação.

---

# 🌎 Objetivo do Projeto

Fortalecer a agricultura familiar e valorizar os conhecimentos tradicionais da comunidade através de uma biblioteca digital acessível, colaborativa e sustentável.

---

# 🚀 Funcionalidades Implementadas

## 📚 Biblioteca Comunitária
- Página inicial institucional
- Informações sobre a comunidade
- Técnicas de plantio
- Cartilhas digitais
- Vídeos comunitários
- Página de conteúdos aprovados

---

## 🛡️ Sistema de Curadoria
- Envio de conteúdos pela comunidade
- Aprovação de conteúdos
- Rejeição de conteúdos
- Exclusão de conteúdos
- Edição de conteúdos enviados
- Área administrativa protegida por login

---

## 📂 Upload de Arquivos
- Upload real de PDFs
- Upload de imagens
- Upload de arquivos diversos
- Armazenamento em servidor local
- Visualização de arquivos pelo curador
- Download/abertura pública de cartilhas aprovadas

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
│   └── uploads/
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
│   ├── editar_conteudo.html
│   └── login.html
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

## 2️⃣ Entre na pasta do projeto

```bash
cd AGROTECA
```

---

## 3️⃣ Instale as dependências

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

### Create
Enviar conteúdo pela plataforma

### Read
Visualizar conteúdos aprovados

### Update
Editar conteúdos enviados

### Delete
Excluir conteúdos

---

# 🎨 Interface

A interface foi desenvolvida com foco em:
- simplicidade;
- acessibilidade;
- identidade amazônica;
- experiência comunitária;
- navegação intuitiva.

---

# 🌱 Impacto Social

A AgroTeca busca:
- preservar conhecimentos tradicionais;
- incentivar agricultura familiar;
- democratizar acesso à informação;
- fortalecer comunidades rurais;
- integrar tecnologia e cultura amazônica.

---

# ✨ Melhorias da Terceira Avaliação

Nesta etapa, o foco foi em identidade visual e pequenos ajustes de usabilidade, sem alterar a arquitetura geral do projeto (Flask + SQLite + templates Jinja, sem JavaScript pesado).

## 🔤 Tipografia
- Substituição da fonte de títulos (antes "Fraunces", uma serifada editorial) por **Plus Jakarta Sans**, mais alinhada a um visual corporativo e moderno.
- Fonte aplicada no título principal "AgroTeca", nos títulos de seção (ex: "Técnicas de plantio"), nos botões e na navegação.
- O corpo do texto continua em Inter, mantendo boa legibilidade para leitura prolongada.

## 🎨 Padronização de botões
- Unificação da cor dos botões de ação principal em laranja com texto branco, em vez da mistura anterior de azul e laranja com texto escuro.
- Aplicado de forma consistente em: "Enviar conhecimento", "Entrar", "Criar Conta", "Enviar para avaliação", "Aprovar" (painel do curador) e "Abrir arquivo" (cartilhas, vídeos e acervo).
- Objetivo: reforçar visualmente qual é a ação principal esperada em cada tela.

## 🏠 Reorganização da página inicial
- Os botões "Enviar conhecimento" e "Biblioteca completa" foram movidos para imediatamente abaixo do texto de abertura (antes ficavam no final da página, depois da lista de seções).
- A mudança aproxima a chamada para ação do primeiro contato do usuário com a página.

## 🔑 Recuperação de senha (fluxo offline)
- Adicionado link "Esqueci minha senha" na tela de login.
- Como o sistema é projetado para funcionar **sem internet** (rede local, Raspberry Pi), não há envio de e-mail de recuperação.
- A nova página `/esqueci-senha` orienta o usuário a procurar um curador da comunidade, que pode redefinir a senha manualmente — solução simples e compatível com o contexto offline do projeto.

---

# 👨‍💻 Desenvolvimento

Projeto acadêmico desenvolvido para o Amazon Hacking, com foco em tecnologia social, sustentabilidade e valorização cultural amazônica.