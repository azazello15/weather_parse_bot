import requests
import datetime
from config import TOKEN, API_KEY
from aiogram import Bot, types, Dispatcher, executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Ну здравствуйте! скажите погоду какого города вы хотите узнать, а я вам все распишу")

@dp.message_handler()
async def get_weather(message: types.Message):

    '''
    для более наглядного ответа я создал словарь для 7 типов погод
    и каждая из них имело значение в виде юнит-кодов соответствующих эмодзи
    '''
    
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    '''
    на данном этапе производился парсинг данных с сайта https://openweathermap.org/api
    с помощью библиотеки requests я произвел запросы и выделив ключевые мометны распарсил JSON-ответ и представил данные в боте
    '''
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        desc = data["weather"][0]["main"]
        if desc in code_to_smile:
            wd = code_to_smile[desc]
        else:
            wd = "Шторы блят открой"

        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day_lendth = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(
            f"****{datetime.datetime.now().strftime('%y-%m_d %H:%M')}****\n"
            f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {day_lendth}\n"
            f"\U0001F918 Хорошего блят дня нах"
        )
    except:
        await message.reply('Проверьте свои знания в географии \U0001F926')


if __name__ == '__main__':
    executor.start_polling(dp)
