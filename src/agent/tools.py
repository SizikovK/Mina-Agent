from langchain_core.tools import tool
import json
from requests import get

@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b




@tool
def parce_cryptocurrencies(cryptocurrency: str, count: int) -> str:
    '''
    Получает информацию о криптовалютах с помощью CoinMarketCap API.
    Args:
        cryptocurrency: str  Название криптовалюты для поиска.
        count: int  Количество криптовалют для получения.

    Returns:
        str: Информация о криптовалютах или сообщение об ошибке.
    '''

    API_KEY = "9f6da3a3c905461e9d0eb20049bc2f6e"
    count = str(count)
    convert = "USD"
    params = f"?start=1&limit={count}&convert={convert}"
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest{params}"
    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    try:
        response = get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        response = ""
        found = False
        
        for elem in data['data']:
            if cryptocurrency.lower() in elem['name'].lower():         
                found = True   
                response += f"{elem['name']} ({elem['symbol']}):\n"
                response += f"  Id: {elem['id']}\n"
                response += f"  Slug: {elem['slug']}\n"
                response += f"  Circulating Supply: {elem['circulating_supply']}\n"
                response += f"  Price: ${elem['quote']['USD']['price']:.2f}\n"
                response += f"  Market Cap: ${elem['quote']['USD']['market_cap']:.2f}\n"
        if not found:
            response += "Криптовалюта не найдена."

    except Exception as e:
        response += f"Error: {e}"

    finally:
        return response

@tool
def parce_weather(city: str) -> str:
    '''
    Получает информацию о погоде в городе с помощью OpenWeatherMap API.
    Args:
        city: str  Название города для получения погоды.

    Returns:
        str: Информация о погоде или сообщение об ошибке.
    '''

    API_KEY = "4af81f1d5c223163c511122479330934"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = get(url)
        response.raise_for_status()
        data = response.json()

        response = ""
        if data['cod'] != 200:
            raise Exception(data['message'])

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed'] + data['wind']['deg'] + data['wind']['gust']

        response = f"Погода в {city}:\n"
        response += f"  Описание: {weather_desc}\n"
        response += f"  Температура: {temp}°C\n"
        response += f"  Ощущается как: {feels_like}°C\n"
        response += f"  Влажность: {humidity}%\n"
        response += f"  Скорость ветра: {wind_speed} м/с"
        response += f"  Угол ветра: {data['wind']['deg']}°\n"
        response += f"  Порыв ветра: {data['wind']['gust']} м/с"

    except Exception as e:
        response = f"Error: {e}"
    
    finally:
        return response

TOOLS = [multiply, add, divide, parce_cryptocurrencies, parce_weather]