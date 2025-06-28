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

### 1. Clone ou baixe o projeto
```bash
# Se usando git
git clone <url-do-repositorio>
cd adm-software

# Ou extraia os arquivos em uma pasta
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
python app.py
```

### 5. Acesse no navegador
```
http://localhost:5000
```

## Estrutura dos Dados

O sistema utiliza os arquivos CSV fornecidos:
- `horarios_metro_ida.csv`: Horários programados no sentido ida
- `horarios_metro_volta.csv`: Horários programados no sentido volta

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

### Considerações
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
