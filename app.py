import yfinance as yf
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd

def obtener_datos(ticker):
    return yf.Ticker(ticker).history(period="max")

def graficar_precio_y_medias_moviles(ax, datos):
    ax.plot(datos["Close"], label="Precio Histórico", zorder=1)
    media_movil_corta = datos["Close"].rolling(window=50).mean()
    media_movil_larga = datos["Close"].rolling(window=200).mean()
    ax.plot(media_movil_corta, label="Media Móvil Corta (50 días)", linestyle='--', linewidth=2, zorder=1)
    ax.plot(media_movil_larga, label="Media Móvil Larga (200 días)", linestyle='--', linewidth=2, zorder=1)

def graficar_ultimo_precio_y_señales(ax, datos, ventana):
    ultimo_precio = datos["Close"].iloc[-1]
    ax.scatter(datos.index[-1], ultimo_precio, color='red', label=f"Último Precio: {ultimo_precio:.2f}", zorder=2)

    # Identificar puntos de cruce y graficar triángulos
    cruzada_alcista = (datos["Close"].rolling(window=50).mean().shift(1) <= datos["Close"].rolling(window=200).mean().shift(1)) & (datos["Close"].rolling(window=50).mean() > datos["Close"].rolling(window=200).mean())
    cruzada_bajista = (datos["Close"].rolling(window=50).mean().shift(1) >= datos["Close"].rolling(window=200).mean().shift(1)) & (datos["Close"].rolling(window=50).mean() < datos["Close"].rolling(window=200).mean())

    # Hacer los triángulos tres veces más grandes
    tamano_triangulos = 3
    ax.scatter(datos.index[cruzada_alcista], datos["Close"][cruzada_alcista], marker='^', color='green', label="Señal Alcista", zorder=3, s=tamano_triangulos*30, edgecolors='black')
    ax.scatter(datos.index[cruzada_bajista], datos["Close"][cruzada_bajista], marker='v', color='red', label="Señal Bajista", zorder=3, s=tamano_triangulos*30, edgecolors='black')

    # Encontrar máximos y mínimos locales
    picos, _ = find_peaks(datos["Close"], distance=ventana)
    valles, _ = find_peaks(-datos["Close"], distance=ventana)

    # Graficar máximos y mínimos locales como líneas horizontales
    ax.hlines(y=datos["Close"].iloc[picos], xmin=datos.index[0], xmax=datos.index[-1], color='blue', label=f'Máximos Locales (Ventana={ventana} días)', zorder=4)
    ax.hlines(y=datos["Close"].iloc[valles], xmin=datos.index[0], xmax=datos.index[-1], color='orange', label=f'Mínimos Locales (Ventana={ventana} días)', zorder=4)


def graficar_volumen(ax, datos):
    ax.bar(datos.index, datos["Volume"], color='blue', alpha=0.5, label="Volumen", zorder=1)

def configurar_grafica(ax, titulo, etiqueta_y):
    ax.set_title(titulo)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(etiqueta_y)
    ax.legend(loc="upper left")  # Mover la leyenda a la parte superior izquierda

# Obtener datos históricos de BTC-USD
datos_btc = obtener_datos("BTC-USD")

# Crear la gráfica con dos subgráficas (una encima de la otra)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

# Graficar precio histórico y medias móviles en la subgráfica superior
graficar_precio_y_medias_moviles(ax1, datos_btc)
graficar_ultimo_precio_y_señales(ax1, datos_btc, ventana=365)  # Ajusta la ventana según sea necesariogit
configurar_grafica(ax1, "Precio Histórico y Medias Móviles", "Precio (USD)")

# Graficar volumen en la subgráfica inferior
graficar_volumen(ax2, datos_btc)
configurar_grafica(ax2, "Volumen de Bitcoin", "Volumen")

# Ajustar la disposición para evitar superposición de etiquetas
plt.tight_layout()

# Mostrar la gráfica
plt.show()
