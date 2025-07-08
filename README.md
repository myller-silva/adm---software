# Sistema de Previsão de Chegada do Metrô

Sistema web desenvolvido em Flask que permite consultar horários do metrô e prever tempos de chegada usando inteligência artificial.

## Funcionalidades

- **Consulta de Horários**: Veja os próximos trens para qualquer estação
- **Previsões IA**: Sistema de machine learning que aprende com dados reais
- **Reports da Comunidade**: Usuários podem reportar horários reais
- **API REST**: Endpoints para integração com outros sistemas
- **Interface Responsiva**: Funciona em desktop e mobile
- **Aprendizado Incremental**: O modelo melhora automaticamente

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite
- **Machine Learning**: TensorFlow
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Processamento de Dados**: Pandas, NumPy
- **Formulários**: Flask-WTF, WTForms

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação e Execução

### Opção 1: Execução com Docker (Recomendado)

#### Pré-requisitos

- Docker instalado
- Docker Compose instalado (opcional, mas recomendado)

#### Usando Docker Compose (Mais Fácil)

```bash
# Iniciar a aplicação
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar a aplicação
docker-compose down
```

#### Usando Scripts de Gerenciamento

**Windows (PowerShell):**

```powershell
# Iniciar
.\docker.ps1 start

# Ver logs
.\docker.ps1 logs

# Parar
.\docker.ps1 stop

# Ver status
.\docker.ps1 status
```

**Linux/Mac (Bash):**

```bash
# Iniciar
./docker.sh start

# Ver logs
./docker.sh logs

# Parar
./docker.sh stop
```

#### Usando Docker Diretamente

```bash
# Construir a imagem
docker build -t metro-prediction-app .

# Executar o container
docker run -d \
  --name metro-app \
  -p 5000:5000 \
  -v "$(pwd)/data:/app/data" \
  metro-prediction-app
```

### Opção 2: Execução Local (Desenvolvimento)

#### 1. Clone ou baixe o projeto

```bash
# Se usando git
git clone <url-do-repositorio>
cd adm-software

# Ou extraia os arquivos em uma pasta
```

#### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Execute a aplicação

```bash
python app.py
```

### Acesso à Aplicação

Após executar (Docker ou local), acesse:

- **URL Principal**: <http://localhost:5000>
- **Documentação da API**: <http://localhost:5000/docs>

## Estrutura dos Dados

O sistema utiliza os arquivos CSV fornecidos:

- `horarios_metro_ida.csv`: Horários programados no sentido Carlito Benevides
- `horarios_metro_volta.csv`: Horários programados no sentido Chico da Silva

### Estações Disponíveis

1. Chico da Silva
2. J.Alencar
3. S.Benedito
4. Benfica
5. Pe.Cicero
6. Porangabussu
7. C.Fernandes
8. J.kubitschek
9. Parangaba
10. V.Pery
11. M.Satiro
12. Mondubim
13. Esperanca
14. Aracape
15. A.Alegre
16. R.Queiroz
17. V.Tavora
18. Maracanaú
19. Jereissati
20. C. Benevides

## Sistema de IA

### Como Funciona

1. **Dados Base**: Horários programados do Metrofor
2. **Coleta de Dados**: Usuários reportam horários reais
3. **Aprendizado**: Rede neural identifica padrões de atraso
4. **Predição**: Sistema prevê horários mais precisos

### Características do Modelo

- **Arquitetura**: Rede neural densa com 3 camadas ocultas
- **Features**: Estação, direção, hora, dia da semana, horário de pico
- **Atualização**: Incremental com novos dados dos usuários
- **Métricas**: Mean Squared Error para atrasos em minutos

## API REST

### Endpoints Disponíveis

#### GET `/api/horarios/{station}/{direction}`

Consulta próximos horários para uma estação

**Exemplo:**

```bash
GET /api/horarios/Parangaba/ida
```

**Resposta:**

```json
{
  "status": "success",
  "station": "Parangaba", 
  "direction": "ida",
  "trains": [
    {
      "scheduled": "14:30",
      "predicted": "14:33", 
      "delay_minutes": 3
    }
  ]
}
```

#### POST `/api/report`

Reporta horário real de chegada

**Exemplo:**

```bash
POST /api/report
Content-Type: application/json

{
  "station": "Parangaba",
  "direction": "ida", 
  "actual_time": "2025-06-28T14:33:00"
}
```

### Documentação Completa

Acesse `/docs` no navegador para ver a documentação completa da API.

## Banco de Dados

### Tabelas

- `scheduled_times`: Horários programados (carregados dos CSVs)
- `real_time_updates`: Reports dos usuários em tempo real

### Arquivos Gerados

- `metro_database.db`: Banco SQLite principal
- `metro_model.h5`: Modelo de IA treinado
- `scaler.pkl`: Normalizador de dados
- `encoders.pkl`: Codificadores de categorias

## Segurança

### Medidas Implementadas

- Validação de entradas contra SQL Injection
- Proteção contra XSS (Cross-Site Scripting)
- Sanitização de dados de formulários
- Validação de tipos e formatos

### Rate Limiting

- Máximo de 100 requisições por minuto por IP
- Reports limitados a horários de até 1 hora atrás

## Interface Web

### Páginas Principais

- **Início** (`/`): Consulta de horários
- **Resultados** (`/consultar`): Exibição de previsões
- **Reportar** (`/reportar`): Formulário para reports
- **API Docs** (`/docs`): Documentação técnica

### Características

- Design responsivo (Bootstrap 5)
- Auto-refresh a cada 30 segundos na página de resultados
- Feedback visual para ações do usuário
- Interface intuitiva e acessível

## Testes

### Testar a Aplicação

1. Inicie o servidor: `python app.py`
2. Acesse `http://localhost:5000`
3. Teste a consulta de horários
4. Teste o report de horários reais
5. Verifique a API em `/docs`

### Testar API Diretamente

```bash
# Consultar horários
curl "http://localhost:5000/api/horarios/Parangaba/ida"

# Reportar horário
curl -X POST "http://localhost:5000/api/report" \
  -H "Content-Type: application/json" \
  -d '{"station":"Parangaba","direction":"ida","actual_time":"2025-06-28T14:33:00"}'
```

## Deploy em Produção

### Deploy com Docker (Recomendado)

O projeto inclui configuração completa do Docker para deploy em produção:

#### Volumes e Persistência

- `./data:/app/data` - Persistência dos dados do banco de dados
- `./logs:/app/logs` - Logs da aplicação (opcional)

#### Variáveis de Ambiente

O container utiliza as seguintes variáveis:

- `FLASK_ENV=production`
- `FLASK_APP=app.py`
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`

#### Comandos Docker Úteis

```bash
# Ver containers em execução
docker ps

# Ver logs do container
docker logs metro-app

# Acessar terminal do container
docker exec -it metro-app bash

# Limpar imagens não utilizadas
docker system prune -a
```

#### Troubleshooting Docker

**Container não inicia:**

1. Verifique os logs: `docker-compose logs`
2. Verifique se a porta 5000 não está em uso
3. Verifique se o Docker tem permissões adequadas

**Dados não persistem:**

1. Certifique-se que o diretório `./data` existe
2. Verifique as permissões do diretório

**Performance lenta:**

1. Aloque mais recursos ao Docker
2. Considere usar uma imagem base mais leve se necessário

### Deploy Tradicional

#### Considerações

1. **Chave Secreta**: Altere `SECRET_KEY` no `app.py`
2. **Banco de Dados**: Considere PostgreSQL para produção
3. **Servidor Web**: Use Gunicorn + Nginx
4. **Monitoramento**: Implemente logs e métricas
5. **Backup**: Configure backup automático do banco

### Exemplo com Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Melhorias Futuras

- [ ] Notificações push para usuários
- [ ] Dashboard administrativo  
- [ ] Histórico de performance do modelo
- [ ] Integração com APIs oficiais do Metrofor
- [ ] App mobile nativo
- [ ] Análise de padrões sazonais
- [ ] Previsão de lotação dos trens

## Contribuição

Para contribuir com o projeto:

1. Reporte bugs ou problemas
2. Sugira melhorias
3. Contribua com dados reais de horários
4. Ajude a testar novas funcionalidades

## Licença

Este projeto foi desenvolvido como sistema de previsão para o Metrofor de Fortaleza-CE.

## Suporte

Para dúvidas ou problemas:

- Verifique a documentação da API em `/docs`
- Consulte este README
- Teste com dados conhecidos primeiro

---

**Desenvolvido para melhorar a experiência dos usuários do Metrô de Fortaleza**
