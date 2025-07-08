# Sistema de Previsão do Metrô de Fortaleza

Sistema web modular para consulta de horários do metrô de Fortaleza com área administrativa para gerenciamento de alertas.

## Estrutura do Projeto

```
adm-software/
├── config.py               # Configurações centralizadas
├── run_new.py              # Ponto de entrada da aplicação
├── database.py             # Módulo de banco de dados legado
├── ml_model.py             # Modelo de Machine Learning
├── requirements.txt        # Dependências Python
├── README.md              # Esta documentação
│
├── app/                   # Aplicação Flask modular
│   ├── __init__.py       # Factory da aplicação
│   ├── blueprints/       # Módulos organizados por funcionalidade
│   │   ├── main.py      # Rotas públicas
│   │   ├── api.py       # API REST
│   │   └── admin.py     # Área administrativa
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── alert.py     # Modelo de alertas
│   │   └── user.py      # Modelo de usuários
│   ├── forms/           # Formulários WTForms
│   │   └── forms.py     # Formulários da aplicação
│   └── utils/           # Utilitários
│       └── timezone.py  # Funções de fuso horário
│
├── data/                  # Dados da aplicação
│   ├── horarios_metro_ida.csv    # Horários sentido Carlito Benevides
│   └── horarios_metro_volta.csv  # Horários sentido Chico da Silva
│
├── database/              # Bancos de dados
│   ├── metro_database.db  # Banco principal (horários)
│   └── metro_admin.db     # Banco administrativo (alertas/usuários)
│
├── models/               # Modelos de Machine Learning
│   ├── metro_model.pkl   # Modelo treinado
│   ├── scaler.pkl        # Normalizador de dados
│   └── encoders.pkl      # Codificadores de categorias
│
├── templates/            # Templates HTML
│   ├── admin/           # Templates administrativos
│   │   ├── base.html    # Base administrativa
│   │   ├── dashboard.html
│   │   ├── alerts_list.html
│   │   ├── alert_form.html
│   │   └── login.html
│   ├── base.html        # Base pública
│   ├── index.html       # Página inicial
│   ├── results.html     # Resultados de consulta
│   ├── alerts.html      # Lista de alertas públicos
│   └── docs.html        # Documentação da API
│
└── static/              # Arquivos estáticos (CSS, JS, imagens)
```

## Configuração Centralizada

O arquivo `config.py` centraliza todas as configurações do projeto:

- **Caminhos de dados**: CSVs de horários
- **Caminhos de banco**: Bancos SQLite
- **Caminhos de modelos**: Arquivos ML .pkl
- **Configurações da aplicação**: Chaves secretas, debug, etc.
- **Lista de estações**: Dados centralizados

## Funcionalidades

### Área Pública
- **Consulta de horários**: Previsão de chegada dos trens por estação
- **Alertas em tempo real**: Informações sobre o status do serviço
- **API REST**: Endpoints para integração com outros sistemas
- **Interface responsiva**: Design adaptativo para dispositivos móveis

### Área Administrativa
- **Gerenciamento de alertas**: Criação, edição e exclusão de alertas
- **Dashboard**: Estatísticas e resumo do sistema
- **Controle de acesso**: Sistema de autenticação seguro
- **Interface intuitiva**: Painel administrativo moderno

## Tecnologias

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de dados**: SQLite
- **ML**: Scikit-learn (modelo de previsão)
- **Arquitetura**: Flask Blueprints (modular)

## Instalação

### Requisitos
- Python 3.8+
- pip

### Configuração

1. **Clone o projeto**:
```bash
git clone <repositorio>
cd adm-software
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Execute o servidor**:
```bash
python run_new.py
```

## Acesso

- **Site público**: http://localhost:5000
- **Área administrativa**: http://localhost:5000/admin
  - Usuário: `admin`
  - Senha: `admin123`
- **Documentação da API**: http://localhost:5000/docs

## API

### Endpoints Principais

- `GET /api/alertas` - Lista todos os alertas
- `GET /api/horarios/<station>/<direction>` - Consulta horários
- `POST /api/report` - Reporta horário real

### Exemplo de Uso

```bash
# Consultar alertas
curl http://localhost:5000/api/alertas

# Consultar horários
curl http://localhost:5000/api/horarios/Parangaba/ida
```

## Organização de Arquivos

### Vantagens da Nova Estrutura

1. **Separação clara**: Dados, modelos, bancos e código organizados
2. **Manutenção facilitada**: Arquivos agrupados por função
3. **Segurança**: .gitignore atualizado para proteger dados sensíveis
4. **Escalabilidade**: Estrutura preparada para crescimento
5. **Configuração centralizada**: Fácil alteração de caminhos e configurações

### Migrações Realizadas

- ✅ CSVs movidos para `data/`
- ✅ Bancos SQLite movidos para `database/`
- ✅ Modelos ML movidos para `models/`
- ✅ Configurações centralizadas em `config.py`
- ✅ Códigos atualizados para usar novos caminhos
- ✅ .gitignore atualizado

## Desenvolvimento

### Estrutura Modular

O sistema utiliza Flask Blueprints para organização modular:

- **main**: Rotas públicas e interface principal
- **api**: Endpoints da API REST
- **admin**: Área administrativa

### Banco de Dados

O sistema utiliza SQLAlchemy com SQLite para persistência:

- **alerts**: Tabela de alertas do sistema
- **users**: Tabela de usuários administrativos

### Modelo de ML

Sistema de previsão usando scikit-learn para estimar tempo de chegada baseado em:
- Horários programados
- Histórico de atrasos
- Condições atuais do sistema

## Configuração de Produção

Para ambiente de produção, configure:

1. **Variáveis de ambiente**:
```bash
export FLASK_ENV=production
export SECRET_KEY=sua-chave-secreta-forte
```

2. **Servidor WSGI** (recomendado: Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua funcionalidade
3. Implemente as mudanças
4. Adicione testes se necessário
5. Faça um pull request

## Licença

MIT License - veja o arquivo LICENSE para detalhes.
