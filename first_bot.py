import requests
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

greet_bot = BotHandler('1172370412:AAFjoR8RvgOQby1b0ZzZb9Y2smt3jZMMMKE')
greetings = ('здравствуй', 'привет', 'ку', 'здорово') #распознавание приветствия

# данные о часовых поясах
UTC_OFFSET = {
    'Москва': 3,
    'Санкт-Петербург': 3,
    'Новосибирск': 7,
    'Екатеринбург': 5,
    'Нижний Новгород': 3,
    'Казань': 3,
    'Челябинск': 5,
    'Омск': 6,
    'Самара': 4,
    'Ростов-на-Дону': 3,
    'Уфа': 5,
    'Красноярск': 7,
    'Воронеж': 3,
    'Пермь': 5,
    'Волгоград': 3,
    'Краснодар': 3,
    'Калининград': 2,
    'Владивосток': 10
}

now = datetime.datetime.now()

# вычисление текущего времени
def what_time(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime("%H:%M")
    return f_time


# получение данных о погоде
def what_weather(city):
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return '<сетевая ошибка>'
    if response.status_code == 200:
        return response.text.strip()
    else:
        return '<ошибка на сервере погоды>'

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text'].lower()
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text in greetings and today == now.day:
                if 6 <= hour < 12:
                    greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
                    today += 1

                elif 12 <= hour < 17:
                    greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
                    today += 1

                elif 17 <= hour < 23:
                    greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
                    today += 1

                new_offset = last_update_id + 1

        elif last_chat_text.startswith == 'погода':
            try:
                mess = last_chat_text.split()[1]
                weather = what_weather(mess)
                greet_bot.send_message(last_chat_id, weather)
            except Exception:
                greet_bot.send_message(last_chat_id, f'Не могу определить погоду в городе {mess}. Попробуй позже.')


        else:
            greet_bot.send_message(last_chat_id, 'Даже не знаю что ответить. Я ещё слишком мало умею((')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

