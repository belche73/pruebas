import pandas as pd
import yfinance as yf
import streamlit as st

from datetime import datetime

# Diccionario con los tickers y sus nombres (igual que en tu ejemplo)
tickers = { ... } # Aquí debes copiar el mismo diccionario que ya tienes

# Función para calcular el ROC
def calculate_roc(data, period):
    end_date = data.index[-1]
    start_date = end_date - pd.DateOffset(months=period)

    if start_date in data.index:
        current_close = data.loc[end_date]
        start_close = data.loc[start_date]
    else:
        start_close = data[data.index < start_date].dropna().iloc[-1]
        current_close = data.loc[end_date]

    return (current_close - start_close) / start_close

# Crear el DataFrame con resultados
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

    data = yf.download(ticker, period='2y', interval='1d')['Close']
    all_dates = pd.date_range(start=data.index.min(), end=data.index.max(), freq='D')
    data = data.reindex(all_dates)
    data = data.ffill()

    roc_1year = calculate_roc(data, 12)
    roc_6months = calculate_roc(data, 6)
    roc_3months = calculate_roc(data, 3)
    roc_1month = calculate_roc(data, 1)

    valor_liquidativo = data.iloc[-1]

    results['id'].append(i)
    results['Activo'].append(ticker)
    results['Nombre Activo'].append(nombre_activo)
    results['Tipo'].append(tipo_activo)
    results['Última Fecha de Cierre'].append(data.index[-1].strftime('%d/%m/%Y'))
    results['Valor liquidativo'].append(valor_liquidativo)
    results['ROC 1 Año'].append(roc_1year)
    results['ROC 6 Meses'].append(roc_6months)
    results['ROC 3 Meses'].append(roc_3months)
    results['ROC 1 Mes'].append(roc_1month)

# Crear DataFrame final
df = pd.DataFrame(results)

# Interfaz con Streamlit
st.title("Dashboard de Rendimiento de Activos")
st.write("Este panel muestra el rendimiento de varios activos financieros.")

# Mostrar DataFrame en la app
st.dataframe(df)  # Permite scroll y ordenamiento

# Opción para descargar el DataFrame como CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Descargar datos como CSV", csv, "datos_activos.csv", "text/csv", key='download-csv')