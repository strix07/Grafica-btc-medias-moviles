import yfinance as yf
import matplotlib.pyplot as plt

datos = yf.Ticker ("BTC-USD").history(period="max")
precio = datos["Close"]
volumen = datos["Volume"]

plt.figure (figsize=(12,6))
plt.plot (precio)
plt.show ()