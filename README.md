# 📈 Streamlit Multi-Exchange Dashboard

Una dashboard Streamlit sicura per monitorare i tuoi portafogli di trading su Kraken, Binance e Capital.com con gestione locale delle credenziali.

## ✨ Caratteristiche Principali

### 🔒 **Sicurezza Avanzata**
- **Credenziali locali**: Le API key rimangono solo in memoria locale del browser
- **Zero server-side storage**: Nessun dato sensibile viene mai inviato al server
- **Auto-cleanup**: Le credenziali si cancellano automaticamente alla chiusura della sessione
- **Read-only API**: Progettato per API key con permessi di sola lettura

### 📊 **Multi-Exchange Support**
- **Kraken**: Integrazione completa via ccxt
- **Binance**: Supporto completo per spot trading
- **Capital.com**: Integrazione base (CFD/Forex)

### 📱 **Dashboard Interattiva**
- Panoramica portafoglio in tempo reale
- Grafici di distribuzione e performance
- Tabelle dettagliate dei balance
- Monitoraggio posizioni aperte
- Prezzi crypto live da CoinGecko

## 🚀 Installazione

### Prerequisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### 1. Clona il Repository
```bash
git clone https://github.com/amaigit/streamlit-multiexchanges-dashboard.git
cd streamlit-multiexchanges-dashboard
```

### 2. Crea un Ambiente Virtuale (Raccomandato)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Avvia l'Applicazione
```bash
streamlit run dashboard.py
```

L'applicazione sarà disponibile su `http://localhost:8501`

## 📦 Dipendenze

Il progetto utilizza le seguenti librerie principali:

```
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
ccxt>=4.0.0
requests>=2.31.0
```

## 🔧 Configurazione Exchange

### Kraken
1. Accedi al tuo account Kraken
2. Vai su **Settings** → **API**
3. Crea una nuova API key con permessi:
   - ✅ **Query Funds** (per vedere i balance)
   - ✅ **Query Open Orders** (per vedere gli ordini)
   - ✅ **Query Closed Orders** (per la cronologia)
   - ❌ **Trade** (NON abilitare per sicurezza)

### Binance
1. Accedi al tuo account Binance
2. Vai su **API Management**
3. Crea una nuova API key con permessi:
   - ✅ **Read Info** (per leggere i dati dell'account)
   - ❌ **Spot & Margin Trading** (NON abilitare)
   - ❌ **Futures** (NON abilitare)

### Capital.com
1. Accedi al tuo account Capital.com
2. Vai su **Settings** → **API**
3. Genera le credenziali API
4. Usa l'account demo per i test iniziali

## 🛡️ Sicurezza

### ⚠️ IMPORTANTE - Linee Guida di Sicurezza

1. **USA SEMPRE API KEY DI SOLA LETTURA**
   - Non abilitare mai permessi di trading
   - Limita i permessi al minimo necessario

2. **Non condividere mai le tue credenziali**
   - Le API key sono personali e riservate
   - Non includerle mai nel codice o nei file di configurazione

3. **Usa account demo per i test**
   - Testa sempre con account demo prima di usare fondi reali
   - Verifica che tutte le funzionalità funzionino correttamente

4. **Monitora l'accesso alle API**
   - Controlla regolarmente i log di accesso sui tuoi exchange
   - Disabilita le API key se non utilizzate

### 🔐 Come Funziona la Sicurezza

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Il tuo        │    │    Dashboard     │    │   Exchange      │
│   Browser       │    │    (Server)      │    │   (Kraken/etc)  │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │                  │    │                 │
│  │Credenziali│  │────┼──────────────────┼───▶│  API Call       │
│  │(Memoria)  │  │    │  (Trasparente)   │    │                 │
│  └───────────┘  │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘

✅ Credenziali solo in memoria locale
✅ Server non vede mai le API key  
✅ Connessione diretta agli exchange
```

## 📋 Utilizzo

### 1. Avvio della Dashboard
```bash
streamlit run dashboard.py
```

### 2. Configurazione Exchange
1. Nella sidebar, espandi la sezione dell'exchange desiderato
2. Inserisci le tue credenziali API
3. Clicca "Connetti" per testare la connessione
4. ✅ Vedrai un indicatore di stato verde se la connessione è riuscita

### 3. Monitoraggio
- **Panoramica**: Valore totale portafoglio e P&L
- **Grafici**: Distribuzione per exchange e performance nel tempo
- **Tabelle**: Balance dettagliati e posizioni aperte
- **Prezzi**: Prezzi crypto in tempo reale

### 4. Gestione Credenziali
- **👁️ Mostra/Nascondi**: Toggle per visualizzare le credenziali
- **Disconnetti**: Rimuovi singoli exchange
- **🗑️ Cancella Tutto**: Rimuovi tutte le credenziali dalla memoria

## 🎯 Funzionalità Avanzate

### Aggiornamento Automatico
- Cache intelligente per ridurre le chiamate API
- Aggiornamento dati ogni 5 minuti
- Pulsante refresh manuale disponibile

### Grafici Interattivi
- Zoom e pan sui grafici
- Tooltip informativi
- Esportazione immagini

### Responsive Design
- Ottimizzato per desktop e tablet
- Layout adattivo
- Sidebar collassabile

## 🔧 Personalizzazione

### Aggiungere Nuovi Exchange
1. Estendi la classe `ExchangeManager`
2. Aggiungi le credenziali in `credentials_manager()`
3. Implementa i metodi specifici per l'exchange

### Modificare le Metriche
- Edita le funzioni in `create_portfolio_chart()`
- Personalizza i calcoli di P&L
- Aggiungi nuove visualizzazioni

## 🐛 Troubleshooting

### Errori Comuni

**"Errore configurazione Exchange"**
```
Soluzioni:
1. Verifica che le API key siano corrette
2. Controlla i permessi dell'API key
3. Assicurati che l'exchange non sia in manutenzione
```

**"Nessun dato visualizzato"**
```
Soluzioni:
1. Clicca "🔄 Aggiorna Dati"
2. Verifica la connessione internet
3. Controlla che le API key non siano scadute
```

**"Errore di connessione"**
```
Soluzioni:
1. Verifica i limiti di rate delle API
2. Controlla il firewall/proxy
3. Prova a riavviare l'applicazione
```

### Log e Debug
```bash
# Avvia con logging dettagliato
streamlit run dashboard.py --logger.level=debug
```

## 🤝 Contribuire

1. Fork il repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT - vedi il file [LICENSE](LICENSE) per i dettagli.

## ⚠️ Disclaimer

- **Questo software è fornito "così com'è" senza garanzie**
- **Non è un consiglio finanziario** - usa solo per monitoraggio
- **I dati potrebbero non essere accurati al 100%** - verifica sempre sui tuoi exchange
- **Gli autori non sono responsabili** per eventuali perdite finanziarie

## 🆘 Supporto

- 📧 **Email**: [Il tuo email]
- 🐛 **Issues**: [GitHub Issues](https://github.com/tuousername/trading-dashboard/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tuousername/trading-dashboard/discussions)

## 🙏 Credits

- [Streamlit](https://streamlit.io/) - Framework per la dashboard
- [ccxt](https://github.com/ccxt/ccxt) - Libreria per exchange crypto
- [Plotly](https://plotly.com/) - Grafici interattivi
- [CoinGecko](https://coingecko.com/) - API prezzi crypto

---

**⭐ Se questo progetto ti è utile, lascia una stella su GitHub!**

**Made with ❤️ for the crypto trading community**
