import yfinance as yf
import matplotlib.pyplot as plt

def obtener_datos(ticker):
    return yf.Ticker(ticker).history(period="max")

def graficar_precio_historico(datos):
    plt.plot(datos["Close"], label="Precio Histórico")

def graficar_ultimo_precio(datos):
    ultimo_precio = datos["Close"].iloc[-1]
    plt.scatter(datos.index[-1], ultimo_precio, color='red', label=f"Último Precio: {ultimo_precio:.2f}")

def configurar_grafica():
    plt.title("Precio Histórico de Bitcoin")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD)")
    plt.legend(loc="upper left")  # Mover la leyenda a la parte superior izquierda
    plt.show()

# Obtener datos históricos de BTC-USD
datos_btc = obtener_datos("BTC-USD")

# Crear la gráfica
plt.figure(figsize=(12, 6))

# Graficar los precios históricos
graficar_precio_historico(datos_btc)

# Obtener y graficar el último precio
graficar_ultimo_precio(datos_btc)

# Configurar etiquetas y leyenda
configurar_grafica()
