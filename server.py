from flask import Flask, request
import time
from random import choice
from string import ascii_letters, digits

app = Flask(__name__)
messages = []
users = {}


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/status")
def server():
    return {
        'server': True,
        'name': 'Text_Messenger',
        'time': time.strftime("%H:%M:%S %d/%m/%y", time.localtime()),
        'count_of_members': len(users),
        'count_of_messages': len(messages)
    }


@app.route("/send_messages")
def send_messages():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username in users:
        if users[username] != password:
            messages.append({'username': 'messenger', 'text': 'Пароль неверный', 'timestamp': time.time()})
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'timestamp': time.time()})

    # чат бот
    name = 'useful_chat_bot'

    if '/useful_chat_bot' in text:
        message = f"Список команд: \n" \
                  f"/generate_password " \
                  f"<длина пароля>     --генерация пароля \n" \
                  f"\n" \
                  f"/heads_or_tails   --подбрасывает монетку \n" \
                  f"\n" \
                  f"/magic_8_ball " \
                  f"<вопрос>   --магический шар с ответами \n" \
                  f"\n" \
                  f"/cubes  --бросок двух кубиков \n" \
                  f"\n" \
                  f"/thinker   --предложит красивую цитату"
        messages.append({'username': name, 'text': message, 'timestamp': time.time()})

    elif '/generate_password' in text:
        length = int(text.split()[1])
        p = ''
        for i in range(length):
            p += choice(ascii_letters + digits)
        messages.append({'username': name, 'text': f"Ваш пароль: {p}", 'timestamp': time.time()})

    elif '/heads_or_tails' in text:
        messages.append({'username': name, 'text': choice(['орёл', 'решка']), 'timestamp': time.time()})

    elif '/magic_8_ball' in text:
        choices = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
                   'Можешь быть уверен в этом', 'Мне кажется — «да»', 'Вероятнее всего',
                   'Хорошие перспективы', 'Знаки говорят — «да»', 'Да',
                   'Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать',
                   'Сейчас нельзя предсказать', 'Соберись и спроси опять', 'Даже не думай',
                   'Мой ответ — «нет»', 'По моим данным — «нет»', 'Перспективы не очень хорошие',
                   'Весьма сомнительно']
        messages.append({'username': name, 'text': choice(choices), 'timestamp': time.time()})

    elif '/cubes' in text:
        dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        messages.append({'username': name, 'text': ' '.join([choice(dashes), choice(dashes)]),
                         'timestamp': time.time()})

    elif '/thinker' in text:
        quotes = ['«Жизнь — как езда на велосипеде. Чтобы сохранить равновесие ты должен двигаться» — Альберт Эйнштейн',
                  '«Если твое счастье зависит от того, как поступают другие, то, '
                  'пожалуй, у тебя действительно есть проблемы» — Ричард Бах',
                  '«Оптимист — это тот, кто находясь между двумя неприятностями всегда '
                  'загадывает желание» — Автор неизвестен',
                  '«Неудача — это просто повод начать еще раз, но уже более мудро» — Генри Форд',
                  '«В каждом человеке противостоят друг другу два волка: злой, несчастный и вечно '
                  'недовольный; и счастливый, довольный и добрый. Побеждает тот, которого ты '
                  'кормишь» — Автор неизвестен',
                  '«Я никогда не сомневался! И это дало мне преимущество над всем миром» — Наполеон Бонапарт',
                  '«Что бы ни случилось, нужно помнить — это всего лишь жизнь, и мы прорвемся!» - '
                  'Дин Кунц. «Темные реки сердца»',
                  '«Человек умирает тогда, когда умирает последнее воспоминание о нем.» - '
                  'Джоан Роулинг, «Гарри Поттер и Орден Феникса»']
        messages.append({'username': name, 'text': choice(quotes), 'timestamp': time.time()})

    return {'ok': True}


@app.route("/get_messages")
def get_messages():
    after = float(request.args['after'])
    result = []
    for message in messages:
        if message['timestamp'] > after:
            result.append(message)
    return {'messages': result}


app.run()
