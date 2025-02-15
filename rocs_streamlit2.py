import pandas as pd
import yfinance as yf
import streamlit as st

from datetime import datetime, timedelta

# Diccionario con los tickers y sus nombres
tickers = {
    '0P00000RQC.F': {'Nombre': 'Vanguard Global Stock Index Fund Investor EUR Accumulation', 'Tipo': 'RV'},
    '0P0001CLDK.F': {'Nombre': 'Fidelity MSCI World Index Fund EUR P Acc', 'Tipo': 'RV'},
    '0P00000SUJ.F': {'Nombre': 'Vanguard U.S. 500 Stk Idx € Acc', 'Tipo': 'RV'},
    '0P0000GACH.F': {'Nombre': 'Seilern World Growth EUR', 'Tipo': 'RV'},
    '0P0000SKSX.F': {'Nombre': 'Threadneedle - Global Smaller Companies', 'Tipo': 'RV'},
    '0P00015OFP.F': {'Nombre': 'Fidelity Funds - Global Technology ', 'Tipo': 'RV'},
    '0P0001OR4G.F': {'Nombre': 'Cinvest Tercio Capital A', 'Tipo': 'RV'},
    '0P0001IK36.F': {'Nombre': 'Hamco Global Value Fund R', 'Tipo': 'RV'},
    '0P0000A96U.F': {'Nombre': 'Fidelity Funds - China Focus Fund', 'Tipo': 'RV'}, #0P0000ZP3T.F
    '0P00012I69.F': {'Nombre': 'Vanguard Global Bond Index Fund EUR Hedged Acc', 'Tipo': 'RF'},
    '0P0000IKFQ.F': {'Nombre': 'Amundi Index Solutions - Amundi Index J.P. Morgan GBI Global Govies AHE-C', 'Tipo': 'RF'},
    '0P00018XCZ.F': {'Nombre': 'FLOSSBACH STORCH BND OPPORTU RT', 'Tipo': 'RF'},
    '0P00012NJH.F': {'Nombre': 'Vanguard Global Short-Term Bond Index Fund EUR Hedged Acc', 'Tipo': 'RF'},
    '0P00000W6H.F': {'Nombre': 'Vanguard US Government Bond Index Fund 10y', 'Tipo': 'RF'},
    '0P0000CV2T.F': {'Nombre': 'Vanguard 20+ Year Euro Treasury Index Fund', 'Tipo': 'RF'},
    '0P0001HFG4.F': {'Nombre': 'DWS Invest Enhanced Commodity Strategy LC', 'Tipo': 'MP'},
    '0P00008Y7H.F': {'Nombre': 'Amundi S.F. - EUR Commodities A EUR ND', 'Tipo': 'MP'},
    '0P0000VOSS.F': {'Nombre': 'Ofi Invest Precious Metals R', 'Tipo': 'GLD'},
    '0P000177J8.F': {'Nombre': 'Amundi Index Solutions - Amundi Index FTSE EPRA NAREIT Global AE-C', 'Tipo': 'REIT'},
    '0P0000TKN0.F': {'Nombre': 'Amundi Funds - Cash EUR G2 EUR (C)', 'Tipo': 'MON'},
    '0P00002BDB.F': {'Nombre': 'La Française Trésorerie ISR', 'Tipo': 'MON'},
    '0P00000B50.F': {'Nombre': 'DWS Euro Ultra Short Fixed Income Fund NC', 'Tipo': 'MON'},
    '0P0000TNHU.F': {'Nombre': 'Amundi Funds - Volatility World A EUR (C)', 'Tipo': 'VOL'},
    '0P0001OR4H.F': {'Nombre': 'Cinvest Tercio Capital B', 'Tipo': 'RV'},
    'BTC-EUR': {'Nombre': 'Bitcoin (Euros)', 'Tipo': 'CRI'},
    '0P00008T36.F': {'Nombre': 'DWS Invest Gold and Precious Metals', 'Tipo': 'GLD'}
}

# Función para calcular el ROC (Rate of Change) utilizando el valor de cierre actual y el primer valor de cierre válido anterior a la fecha "start_date"

def calculate_roc(data, period):
    end_date = data.index[-1]  # Fecha actual
    start_date = end_date - pd.DateOffset(months=period)  # Fecha "period" meses antes

    # Verificar si start_date está en el índice del DataFrame
    if start_date in data.index:
        current_close = data.loc[end_date].iloc[0]  # Valor de cierre actual
        start_close = data.loc[start_date].iloc[0]  # Valor de cierre "period" meses antes
    else:
        # Obtener el primer valor de cierre válido anterior a start_date
        start_close = data[data.index < start_date].dropna().iloc[-1]
        current_close = data.loc[end_date].iloc[0]  # Valor de cierre actual

    return (current_close - start_close) / start_close

# Diccionario para almacenar los resultados
results = {
    'id': [],
    'Activo': [],
    'Nombre Activo': [],
    'Tipo': [],
    'Última Fecha de Cierre': [],
    'Valor liquidativo': [],
    'ROC 1 Año': [],
    'ROC 6 Meses': [],
    'ROC 3 Meses': [],
    'ROC 1 Mes': []
}

for i, (ticker, data_ticker) in enumerate(tickers.items(), start=1):
    nombre_activo = data_ticker['Nombre']
    tipo_activo = data_ticker['Tipo']

    # Descargar datos de Yahoo Finance
    data = yf.download(ticker, period='2y', interval='1d')['Close']
    all_dates = pd.date_range(start=data.index.min(), end=data.index.max(), freq='D')
    data = data.reindex(all_dates)
    data = data.ffill()

    # Calcular ROC
    roc_1year = round(calculate_roc(data, 12) * 100,2)
    roc_6months = round(calculate_roc(data, 6) * 100,2)
    roc_3months = round(calculate_roc(data, 3) * 100,2)
    roc_1month = round(calculate_roc(data, 1) * 100,2)

    # Almacenar el valor liquidativo de la última fecha de cierre
    valor_liquidativo = data.iloc[-1]
    valor_liquidativo = valor_liquidativo.iloc[0]
    # Almacenar resultados
    results['id'].append(i)
    results['Tipo'].append(tipo_activo)
    results['Activo'].append(ticker)
    results['Nombre Activo'].append(nombre_activo)
    results['Última Fecha de Cierre'].append(data.index[-1].strftime('%d/%m/%Y'))
    results['Valor liquidativo'].append(valor_liquidativo)
    results['ROC 1 Año'].append(roc_1year)
    results['ROC 6 Meses'].append(roc_6months)
    results['ROC 3 Meses'].append(roc_3months)
    results['ROC 1 Mes'].append(roc_1month)

# Crear DataFrame con los resultados
df = pd.DataFrame(results)

# Aplicar colores de fondo (fondos rojos y verdes para valores negativos y positivos)
def highlight_roc(s):
    color = 'background-color: #d4f7d4' if s > 0 else 'background-color: #f7d4d4' if s < 0 else ''
    return color

styled_df = df.style.applymap(highlight_roc, subset=['ROC 1 Año', 'ROC 6 Meses', 'ROC 3 Meses', 'ROC 1 Mes'])

st.title("Dashboard de Rendimiento de Activos")
st.write("Este panel muestra el rendimiento de varios activos financieros con resaltado de ROC.")

# Mostrar con scroll y ordenamiento interactivo
st.dataframe(
    styled_df,  
    height=600,  # Ajusta la altura para scroll
    use_container_width=True  
)
