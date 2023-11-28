import yfinance as yf
import matplotlib.pyplot as plt

def obtener_datos(ticker):
    return yf.Ticker(ticker).history(period="max")

def graficar_precio_historico(ax, datos):
    ax.plot(datos["Close"], label="Precio Histórico", zorder=1)

def graficar_ultimo_precio(ax, datos):
    ultimo_precio = datos["Close"].iloc[-1]
    ax.scatter(datos.index[-1], ultimo_precio, color='red', label=f"Último Precio: {ultimo_precio:.2f}", zorder=2)

def graficar_medias_moviles(ax, datos):
    media_movil_corta = datos["Close"].rolling(window=50).mean()
    media_movil_larga = datos["Close"].rolling(window=200).mean()
    ax.plot(media_movil_corta, label="Media Móvil Corta (50 días)", linestyle='--', linewidth=2, zorder=1)
    ax.plot(media_movil_larga, label="Media Móvil Larga (200 días)", linestyle='--', linewidth=2, zorder=1)
    
    # Identificar puntos de cruce y graficar triángulos
    cruzada_alcista = (media_movil_corta.shift(1) <= media_movil_larga.shift(1)) & (media_movil_corta > media_movil_larga)
    cruzada_bajista = (media_movil_corta.shift(1) >= media_movil_larga.shift(1)) & (media_movil_corta < media_movil_larga)

    # Hacer los triángulos tres veces más grandes
    tamano_triangulos = 3

    ax.scatter(datos.index[cruzada_alcista], datos["Close"][cruzada_alcista], marker='^', color='green', label="Señal Alcista", zorder=3, s=tamano_triangulos*30, edgecolors='black')
    ax.scatter(datos.index[cruzada_bajista], datos["Close"][cruzada_bajista], marker='v', color='red', label="Señal Bajista", zorder=3, s=tamano_triangulos*30, edgecolors='black')

def graficar_volumen(ax, datos):
    ax.bar(datos.index, datos["Volume"], color='blue', alpha=0.5, label="Volumen", zorder=1)

def configurar_grafica(ax):
    ax.set_title("Precio Histórico y Volumen de Bitcoin con Señales de Trading")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (USD)")
    ax.legend(loc="upper left")  # Mover la leyenda a la parte superior izquierda

# Obtener datos históricos de BTC-USD
datos_btc = obtener_datos("BTC-USD")

# Crear la gráfica con dos subgráficas (una encima de la otra)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

# Graficar precio histórico en la subgráfica superior
graficar_precio_historico(ax1, datos_btc)
graficar_ultimo_precio(ax1, datos_btc)
graficar_medias_moviles(ax1, datos_btc)

# Configurar etiquetas y leyenda para la subgráfica superior
configurar_grafica(ax1)

# Graficar volumen en la subgráfica inferior
graficar_volumen(ax2, datos_btc)

# Configurar etiquetas para la subgráfica inferior
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Volumen")

# Ajustar la disposición para evitar superposición de etiquetas
plt.tight_layout()

# Mostrar la gráfica
plt.show()
