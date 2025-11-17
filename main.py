import time
import ccxt
import requests

# ========== НАСТРОЙКИ ==========
TELEGRAM_BOT_TOKEN = "8561518080:AAEvf-gv_l7F-_jenwkLcO6LhXczcKHij70"  # <-- вставь сюда
TELEGRAM_CHAT_ID = "845312449"         # <-- вставь сюда
PRICE_DIFF = 0.1                          # % разницы, чтобы отправлять сигнал

SYMBOLS = [
    "LIGHTUSDT", "BANANAS31USDT", "RESOLVUSDT", "RESOLVUSDC", "WCTUSDT",
    "PUFFERUSDT", "AWEUSDT", "NILUSDT", "ASTERUSDT", "AVLUSDT",
    "PIGGYUSDT", "QUSDT", "HOMEUSDT", "STRKUSDC", "STRKUSDT",
    "SIGNUSDT", "OBOLUSDT", "EVAUSDT", "CROSSUSDT", "SOONUSDT",
    "USELESSUSDT", "LYNUSDT"
]

# ========== БИРЖИ ==========
bybit = ccxt.bybit()
okx = ccxt.okx()


# ========== ФУНКЦИЯ ДЛЯ ОТПРАВКИ УВЕДОМЛЕНИЙ ==========
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, json=payload)


# ========== ЦИКЛ МОНИТОРИНГА ==========
def get_price(exchange, symbol):
    try:
        data = exchange.fetch_ticker(symbol)
        return data["last"]
    except Exception:
        return None


send_message("🚀 Бот запущен и мониторит цены Bybit ↔ OKX")

while True:
    for s in SYMBOLS:
        sym = s.replace("USDT", "/USDT").replace("USDC", "/USDC")

        price_bybit = get_price(bybit, sym)
        price_okx = get_price(okx, sym)

        if price_bybit and price_okx:
            diff = abs(price_bybit - price_okx) / ((price_bybit + price_okx) / 2) * 100

            if diff >= PRICE_DIFF:
                msg = (
                    f"⚡ Арбитраж найден!\n"
                    f"Монета: {s}\n"
                    f"Bybit: {price_bybit}\n"
                    f"OKX: {price_okx}\n"
                    f"Разница: {diff:.2f}%\n\n"
                    f"👉 Дешевле: {'Bybit' if price_bybit < price_okx else 'OKX'}\n"
                    f"👉 Дороже: {'OKX' if price_bybit < price_okx else 'Bybit'}\n"
                )
                send_message(msg)

    time.sleep(5)
