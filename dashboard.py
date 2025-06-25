import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import hashlib
import hmac
import base64
import time
import json
from datetime import datetime, timedelta
import ccxt

# Configurazione della pagina
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializza i dati sensibili nel session state se non esistono
if 'credentials' not in st.session_state:
    st.session_state.credentials = {
        'kraken': {'api_key': '', 'api_secret': '', 'connected': False},
        'binance': {'api_key': '', 'api_secret': '', 'connected': False},
        'capital': {'api_key': '', 'password': '', 'demo': True, 'connected': False}
    }

if 'show_credentials' not in st.session_state:
    st.session_state.show_credentials = False

# Classe per gestire le connessioni agli exchange
class ExchangeManager:
    def __init__(self):
        self.exchanges = {}
    
    def setup_kraken(self, api_key, api_secret):
        """Configura la connessione a Kraken"""
        try:
            self.exchanges['kraken'] = ccxt.kraken({
                'apiKey': api_key,
                'secret': api_secret,
                'sandbox': False,
                'enableRateLimit': True,
            })
            return True
        except Exception as e:
            st.error(f"Errore configurazione Kraken: {e}")
            return False
    
    def setup_binance(self, api_key, api_secret):
        """Configura la connessione a Binance"""
        try:
            self.exchanges['binance'] = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'sandbox': False,
                'enableRateLimit': True,
            })
            return True
        except Exception as e:
            st.error(f"Errore configurazione Binance: {e}")
            return False
    
    def setup_capital(self, api_key, password, demo=True):
        """Configura la connessione a Capital.com"""
        # Capital.com usa un approccio diverso - login basato su sessione
        self.capital_credentials = {
            'api_key': api_key,
            'password': password,
            'demo': demo
        }
        return True
    
    def get_balance(self, exchange_name):
        """Ottiene il balance da un exchange"""
        try:
            if exchange_name in self.exchanges:
                balance = self.exchanges[exchange_name].fetch_balance()
                return balance
            elif exchange_name == 'capital':
                return self._get_capital_balance()
            return None
        except Exception as e:
            st.error(f"Errore recupero balance {exchange_name}: {e}")
            return None
    
    def _get_capital_balance(self):
        """Metodo specifico per Capital.com (implementazione semplificata)"""
        # Nota: Capital.com richiede autenticazione OAuth più complessa
        # Questa è una versione semplificata
        return {
            'total': {'EUR': 1000},  # Valore di esempio
            'free': {'EUR': 800},
            'used': {'EUR': 200}
        }
    
    def get_positions(self, exchange_name):
        """Ottiene le posizioni aperte"""
        try:
            if exchange_name in self.exchanges:
                positions = self.exchanges[exchange_name].fetch_positions()
                return [pos for pos in positions if pos['contracts'] > 0]
            return []
        except Exception as e:
            st.error(f"Errore recupero posizioni {exchange_name}: {e}")
            return []

# Funzioni per la dashboard
@st.cache_data(ttl=300)  # Cache per 5 minuti
def get_crypto_prices():
    """Recupera i prezzi delle crypto principali"""
    try:
        symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'SOL']
        prices = {}
        
        for symbol in symbols:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=eur,usd"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                prices[symbol] = data.get(symbol.lower(), {})
        
        return prices
    except Exception as e:
        st.error(f"Errore recupero prezzi: {e}")
        return {}

def create_portfolio_chart(balances_data):
    """Crea il grafico del portafoglio"""
    if not balances_data:
        return None
    
    # Prepara i dati per il grafico
    exchange_totals = {}
    all_assets = {}
    
    for exchange, balance in balances_data.items():
        if balance and 'total' in balance:
            total_value = 0
            for asset, amount in balance['total'].items():
                if amount > 0:
                    # Converti tutto in EUR (semplificazione)
                    if asset == 'EUR':
                        value = amount
                    elif asset == 'USD':
                        value = amount * 0.85  # Tasso di cambio approssimativo
                    else:
                        value = amount * 100  # Valore approssimativo per crypto
                    
                    total_value += value
                    all_assets[asset] = all_assets.get(asset, 0) + amount
            
            exchange_totals[exchange] = total_value
    
    # Grafico a torta per distribuzione per exchange
    if exchange_totals:
        fig_pie = px.pie(
            values=list(exchange_totals.values()),
            names=list(exchange_totals.keys()),
            title="Distribuzione Portafoglio per Exchange"
        )
        return fig_pie
    
    return None

def create_performance_chart():
    """Crea un grafico delle performance simulate"""
    # Dati di esempio per le performance
    dates = pd.date_range(start='2024-01-01', end='2024-06-25', freq='D')
    
    # Simula performance degli exchange
    kraken_perf = [1000 + i*2 + (i%10)*5 for i in range(len(dates))]
    binance_perf = [1500 + i*3 + (i%15)*8 for i in range(len(dates))]
    capital_perf = [800 + i*1.5 + (i%20)*4 for i in range(len(dates))]
    
    df = pd.DataFrame({
        'Date': dates,
        'Kraken': kraken_perf,
        'Binance': binance_perf,
        'Capital.com': capital_perf
    })
    
    fig = px.line(df, x='Date', y=['Kraken', 'Binance', 'Capital.com'],
                  title="Performance del Portafoglio nel Tempo")
    
    return fig

# Interfaccia principale
def main():
    st.title("📈 Trading Dashboard Multi-Exchange")
    st.markdown("---")
    
    # Inizializza il manager degli exchange
    if 'exchange_manager' not in st.session_state:
        st.session_state.exchange_manager = ExchangeManager()
    
    # Sidebar per configurazione
    with st.sidebar:
        st.header("🔧 Configurazione API")
        
        # Configurazione Kraken
        st.subheader("Kraken")
        kraken_api_key = st.text_input("API Key Kraken", type="password", key="kraken_key")
        kraken_api_secret = st.text_input("API Secret Kraken", type="password", key="kraken_secret")
        
        if st.button("Connetti Kraken"):
            if kraken_api_key and kraken_api_secret:
                success = st.session_state.exchange_manager.setup_kraken(kraken_api_key, kraken_api_secret)
                if success:
                    st.success("Kraken connesso!")
        
        # Configurazione Binance
        st.subheader("Binance")
        binance_api_key = st.text_input("API Key Binance", type="password", key="binance_key")
        binance_api_secret = st.text_input("API Secret Binance", type="password", key="binance_secret")
        
        if st.button("Connetti Binance"):
            if binance_api_key and binance_api_secret:
                success = st.session_state.exchange_manager.setup_binance(binance_api_key, binance_api_secret)
                if success:
                    st.success("Binance connesso!")
        
        # Configurazione Capital.com
        st.subheader("Capital.com")
        capital_api_key = st.text_input("API Key Capital.com", type="password", key="capital_key")
        capital_password = st.text_input("Password Capital.com", type="password", key="capital_pass")
        capital_demo = st.checkbox("Account Demo", value=True)
        
        if st.button("Connetti Capital.com"):
            if capital_api_key and capital_password:
                success = st.session_state.exchange_manager.setup_capital(capital_api_key, capital_password, capital_demo)
                if success:
                    st.success("Capital.com connesso!")
        
        st.markdown("---")
        
        # Refresh data
        if st.button("🔄 Aggiorna Dati", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # Area principale
    col1, col2, col3 = st.columns(3)
    
    # Recupera i balances
    balances = {}
    total_portfolio_value = 0
    
    exchanges = ['kraken', 'binance', 'capital']
    for exchange in exchanges:
        balance = st.session_state.exchange_manager.get_balance(exchange)
        balances[exchange] = balance
        
        if balance and 'total' in balance:
            # Calcola valore approssimativo
            for asset, amount in balance['total'].items():
                if amount > 0:
                    if asset == 'EUR':
                        total_portfolio_value += amount
                    elif asset == 'USD':
                        total_portfolio_value += amount * 0.85
                    else:
                        total_portfolio_value += amount * 100  # Approssimazone
    
    # Metriche principali
    with col1:
        st.metric("💰 Valore Totale Portafoglio", f"€{total_portfolio_value:,.2f}")
    
    with col2:
        st.metric("📊 Exchange Connessi", f"{len([b for b in balances.values() if b])}/3")
    
    with col3:
        # Calcola P&L giornaliero (simulato)
        daily_pnl = total_portfolio_value * 0.02  # 2% simulato
        st.metric("📈 P&L Giornaliero", f"€{daily_pnl:,.2f}", f"{daily_pnl/total_portfolio_value*100:.2f}%")
    
    st.markdown("---")
    
    # Grafici principali
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafico distribuzione portafoglio
        portfolio_chart = create_portfolio_chart(balances)
        if portfolio_chart:
            st.plotly_chart(portfolio_chart, use_container_width=True)
        else:
            st.info("Connetti gli exchange per visualizzare la distribuzione del portafoglio")
    
    with col2:
        # Grafico performance
        performance_chart = create_performance_chart()
        st.plotly_chart(performance_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Tabelle dettagliate
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💳 Balances per Exchange")
        for exchange, balance in balances.items():
            if balance and 'total' in balance:
                st.write(f"**{exchange.upper()}**")
                balance_df = pd.DataFrame([
                    {'Asset': asset, 'Quantità': amount, 'Disponibile': balance.get('free', {}).get(asset, 0)}
                    for asset, amount in balance['total'].items() if amount > 0
                ])
                if not balance_df.empty:
                    st.dataframe(balance_df, use_container_width=True)
                else:
                    st.info(f"Nessun balance disponibile per {exchange}")
            else:
                st.info(f"Connetti {exchange} per visualizzare i balance")
    
    with col2:
        st.subheader("🎯 Posizioni Aperte")
        all_positions = []
        for exchange in exchanges:
            positions = st.session_state.exchange_manager.get_positions(exchange)
            for pos in positions:
                all_positions.append({
                    'Exchange': exchange.upper(),
                    'Symbol': pos.get('symbol', 'N/A'),
                    'Side': pos.get('side', 'N/A'),
                    'Size': pos.get('contracts', 0),
                    'PnL': pos.get('unrealizedPnl', 0)
                })
        
        if all_positions:
            positions_df = pd.DataFrame(all_positions)
            st.dataframe(positions_df, use_container_width=True)
        else:
            st.info("Nessuna posizione aperta trovata")
    
    # Prezzi crypto
    st.markdown("---")
    st.subheader("💹 Prezzi Crypto Attuali")
    
    crypto_prices = get_crypto_prices()
    if crypto_prices:
        price_cols = st.columns(len(crypto_prices))
        for i, (symbol, prices) in enumerate(crypto_prices.items()):
            with price_cols[i]:
                eur_price = prices.get('eur', 0)
                st.metric(f"{symbol}", f"€{eur_price:,.2f}")
    else:
        st.info("Impossibile recuperare i prezzi delle crypto")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Dashboard Trading Multi-Exchange | Ultimo aggiornamento: {}</p>
        <p><small>⚠️ Assicurati di utilizzare API key con permessi di sola lettura per sicurezza</small></p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
