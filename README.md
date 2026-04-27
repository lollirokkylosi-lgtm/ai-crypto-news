# 🤖 AI & Crypto News Digest

Sistema avanzato per l'aggregazione automatica, l'analisi e la distribuzione di notizie su Intelligenza Artificiale e Criptovalute.

## 🌟 Caratteristiche

- **Multi-source**: Raccoglie da 15+ feed RSS, GitHub releases
- **Smart Scoring**: Algoritmo personalizzato per prioritizzare notizie rilevanti  
- **AI Summarization**: Genera riassunti in italiano con OpenAI/Anthropic
- **Duplicates Removal**: Elimina articoli simili o duplicati (85% similarità)
- **Multi-format Output**: HTML, Email, Discord
- **Personalizzazione**: Aggiungi facilmente nuove fonti RSS
- **Categorie automatiche**: AI, Crypto, Tech, Altro
- **Directory Tool**: 🤖 AI Tools + 🪙 Crypto Tools aggiornati

## 📦 Installazione

### 1. Requisiti
```bash
Python 3.8+
```

### 2. Configurazione
```bash
cd ai-crypto-news
pip install -r requirements.txt
cp .env.example .env
# Modifica .env con le tue API keys (opzionale)
```

### 3. Esecuzione

**Modalità Test:**
```bash
python main.py --dry-run
```

**Modalità Normale:**
```bash
python main.py
```

**Con Directory Tool:**
```bash
python main.py --with-tools
```

### Opzioni
```bash
python main.py --days 2    # Ultimi 2 giorni
python main.py --limit 5   # Solo 5 articoli
python main.py --config custom.yaml
```

## 🔧 Configurazione

Modifica `config.yaml` per personalizzare:

- **Fonti RSS**: Aggiungi i tuoi feed preferiti
- **Scoring**: Regola pesi e soglie  
- **Output**: Attiva/disattiva canali
- **AI**: Configura modello e prompt
- **Tools**: Abilita directory tool

### Fonti Incluse (Default)

**AI/ML:**
- OpenAI Blog, Anthropic News, MIT Tech Review
- Hacker News AI, TechCrunch AI, VentureBeat AI, Wired AI

**Crypto:**
- CoinDesk, CoinTelegraph, The Block, Decrypt, CryptoSlate

**GitHub:**
- GPT, vLLM, LangChain, Ollama, Bitcoin, Ethereum

## 🔧 Come Funziona

```
1. Fetch     → RSS + GitHub → Articoli raw
   ↓
2. Dedup     → Rimuove duplicati (85% similarità)
   ↓
3. Score     → Calcola rilevanza (0-10)
   ↓
4. Filter    → Toglie sotto la soglia (6.0)
   ↓
5. Summarize → Genera riassunti con IA
   ↓
6. Output    → HTML + Email + Discord
```

## 📊 Algoritmo di Scoring

Ogni articolo riceve un punteggio base **5.0**:

| Fattore | Bonus/Penalty |
|---------|---------------|
| Fonte prioritaria | +2.0 |
| Meno di 24h | +1.5 |
| AI keyword | +0.5-0.8 |
| Crypto keyword | +0.8-1.0 |
| Summary lunga | +0.5 |
| Dominio non affidabile | -1.0 |
| Oltre 7 giorni | -2.0 |

**Soglia minima**: 6.0 (configurabile)

## 🤖 AI & Crypto Tools Directory

Per generare una pagina con i migliori tool AI e Crypto:

```bash
python main.py --with-tools
```

La directory include:
- **🤖 Tool AI**: LLM, generatori immagini, strumenti ML
- **🪙 Tool Crypto**: Exchange, wallet, protocolli DeFi  
- **📊 Dati**: TVL, rating, popolarità
- **🔗 Link diretti** ai siti

Output: `output/tools_YYYYMMDD.html`

### Fonti Dati Tool
- Product Hunt (trending AI/Crypto)
- GitHub (repository popolari)
- CoinGecko (exchange e protocolli)
- DeFiLlama (TVL protocolli)

## 🎯 Output

### HTML Page
Pagina web responsive con:
- Statistiche in alto
- Cards per ogni articolo
- Categorie colorate (AI 🟢, Crypto 🟠)
- Link diretti

### Email Digest
Inviata via SMTP con:
- Formattazione HTML
- Sintesi articoli
- Link originali

### Discord
Embed con:
- Top 5 articoli
- Score e categoria
- Link immediati

## 🔐 Sicurezza & Privacy

- **Niente chiavi nel Git**: Tutto in `.env`
- **Rate limit**: Gestione API GitHub
- **Error handling**: Fallback senza IA
- **Dati locali**: SQLite, nessun cloud

## ⚙️ Automazione

### Linux/Mac (Cron)
```bash
0 8 * * * cd /path/to/ai-crypto-news && python main.py >> logs/digest.log 2>&1
```

### Windows (Task Scheduler)
1. Task Scheduler → Create Task
2. Trigger: Daily 8:00
3. Action: `python main.py`

## 📈 Estensioni Possibili

- Telegram bot notifications
- Twitter/KOL monitoring
- Web scraping avanzato
- Machine learning classificazione
- Interfaccia web con Flask
- API REST pubblica

## 📞 Supporto & Troubleshooting

**Problemi comuni:**
- Timeout RSS: Aumentare timeout in `fetcher.py`
- Rate limit GitHub: Ottenere token
- Nessun riassunto IA: Configurare API key

**Log:**
```bash
tail -f ai_crypto_news.log
```

## 📄 Licenza

MIT - Liberamente modificabile

--- Sviluppato con ❤️ per la community OpenClaw ---

--- Happy Coding! 🚀 ---
