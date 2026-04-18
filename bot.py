import os, json, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")

# ─── Film data ────────────────────────────────────────────────────────────────
RESULTS = {
1: {"title": "Драмы", "films": [{"title": "Drama", "year": 2026, "director": "—", "cast": "—", "platform": "—", "desc": "Скоро в кино.", "imdb": "https://www.imdb.com/find/?q=Drama+2026", "kp": "https://www.kinopoisk.ru/index.php?kp_query=Drama+2026"}, {"title": "Project Hail Mary", "year": 2026, "director": "Phil Lord, Christopher Miller", "cast": "Ryan Gosling, Sandra Hüller", "platform": "Amazon MGM", "desc": "Астронавт просыпается один на корабле без памяти — и обнаруживает что это последний шанс спасти Землю. Тяжело и светло одновременно.", "imdb": "https://www.imdb.com/title/tt14080742/", "kp": "https://www.kinopoisk.ru/film/5369000/"}, {"title": "Wuthering Heights", "year": 2026, "director": "Emerald Fennell", "cast": "Margot Robbie, Jacob Elordi", "platform": "Warner Bros.", "desc": "Феннел переосмысляет Бронте: тёмная история одержимости, в которой любовь и разрушение неотделимы.", "imdb": "https://www.imdb.com/title/tt28155786/", "kp": "https://www.kinopoisk.ru/film/5420100/"}, {"title": "A House of Dynamite", "year": 2025, "director": "Kathryn Bigelow", "cast": "Idris Elba, Rebecca Ferguson, Greta Lee, Jared Harris", "platform": "Netflix", "desc": "Неизвестный противник выпускает межконтинентальную ракету по Чикаго — и у США есть минуты, чтобы решить: отвечать или нет. Байгело возвращается после 8 лет молчания. Венеция 2025.", "imdb": "https://www.imdb.com/find/?q=A+House+of+Dynamite", "kp": "https://www.kinopoisk.ru/index.php?kp_query=A+House+of+Dynamite"}, {"title": "Bugonia", "year": 2025, "director": "Yorgos Lanthimos", "cast": "Emma Stone, Jesse Plemons", "platform": "Focus Features", "desc": "Два фанатика-конспиролога похищают CEO крупной корпорации. Лантимос снимает насилие с неожиданной нежностью.", "imdb": "https://www.imdb.com/title/tt28363360/", "kp": "https://www.kinopoisk.ru/film/5400200/"}, {"title": "Caught Stealing", "year": 2025, "director": "Darren Aronofsky", "cast": "Austin Butler, Regina King, Zoë Kravitz, Bad Bunny", "platform": "Sony Pictures", "desc": "Бывший бейсбольный вундеркинд работает барменом в Нью-Йорке — пока сосед не попросил присмотреть за котом. Аронофски снимает чёрную криминальную комедию в духе 90-х.", "imdb": "https://www.imdb.com/title/tt14849194/", "kp": "https://www.kinopoisk.ru/film/5253000/"}, {"title": "Eddington", "year": 2025, "director": "Ari Aster", "cast": "Joaquin Phoenix, Pedro Pascal, Emma Stone", "platform": "A24 / HBO Max", "desc": "Маленький город Нью-Мексико, 2020: пандемия, выборы шерифа, и Америка пожирает саму себя. Ари Астер снимает политическую сатиру.", "imdb": "https://www.imdb.com/title/tt30472964/", "kp": "https://www.kinopoisk.ru/film/5430000/"}, {"title": "F1: The Movie", "year": 2025, "director": "Joseph Kosinski", "cast": "Brad Pitt, Damson Idris, Kerry Condon", "platform": "Apple Original Films", "desc": "Легенда Формулы-1 возвращается из отставки тренировать молодого гонщика. Снято на реальных Гран-при.", "imdb": "https://www.imdb.com/title/tt8790086/", "kp": "https://www.kinopoisk.ru/film/5410000/"}, {"title": "Father Mother Sister Brother", "year": 2025, "director": "Jim Jarmusch", "cast": "Adam Driver, Cate Blanchett, Charlotte Rampling", "platform": "A24", "desc": "Трёхчастная антология о семьях: брат и сестра, мать и дочь, близнецы. Джармуш в режиме тихой радости. Золотой лев Венеции.", "imdb": "https://www.imdb.com/title/tt30472964/", "kp": "https://www.kinopoisk.ru/film/5452001/"}, {"title": "Frankenstein", "year": 2025, "director": "Guillermo del Toro", "cast": "Oscar Isaac, Mia Goth, Christoph Waltz", "platform": "Netflix", "desc": "Del Toro переосмысляет Мэри Шелли: история не монстра, а создателя и брошенного дитя.", "imdb": "https://www.imdb.com/title/tt32100001/", "kp": "https://www.kinopoisk.ru/film/5448000/"}, {"title": "Hamnet", "year": 2025, "director": "Chloé Zhao", "cast": "Jessie Buckley, Paul Mescal", "platform": "Focus Features", "desc": "Шекспир теряет сына — и пишет «Гамлета». Не о великом авторе, а о невыносимом горе. Оскар за лучшую женскую роль.", "imdb": "https://www.imdb.com/title/tt28241249/", "kp": "https://www.kinopoisk.ru/film/5369001/"}, {"title": "Highest 2 Lowest", "year": 2025, "director": "Spike Lee", "cast": "Denzel Washington, Jeffrey Wright, A$AP Rocky, Ice Spice", "platform": "A24 / Apple TV+", "desc": "Ремейк «Рая и ада» Куросавы: музыкальный магнат стоит перед моральным выбором — пожертвовать состоянием ради чужого ребёнка или нет. Пятое сотрудничество Ли и Вашингтона. Канны 2025.", "imdb": "https://www.imdb.com/title/tt32469864/", "kp": "https://www.kinopoisk.ru/film/5369002/"}, {"title": "If I Had Legs I'd Kick You", "year": 2025, "director": "Mary Bronstein", "cast": "Rose Byrne, Conan O'Brien, A$AP Rocky", "platform": "A24", "desc": "Мать-терапевт: потолок рушится, ребёнок орёт, жизнь идёт ко дну. Жестокая, смешная и точная комедия о материнстве.", "imdb": "https://www.imdb.com/title/tt28827000/", "kp": "https://www.kinopoisk.ru/film/5430001/"}, {"title": "It Was Just an Accident", "year": 2025, "director": "Jafar Panahi", "cast": "Vahid Mobasseri", "platform": "Neon", "desc": "Механик убеждён, что к нему зашёл человек, пытавший его в тюрьме. Пальмовая ветвь Каннского МКФ.", "imdb": "https://www.imdb.com/title/tt30000001/", "kp": "https://www.kinopoisk.ru/film/5450001/"}, {"title": "Marty Supreme", "year": 2025, "director": "Josh Safdie", "cast": "Timothée Chalamet, Gwyneth Paltrow, Tyler the Creator", "platform": "A24", "desc": "Байопик о пинг-понговом prodigy: азарт, скандалы, одержимость победой.", "imdb": "https://www.imdb.com/title/tt32469864/", "kp": "https://www.kinopoisk.ru/film/5369003/"}, {"title": "No Other Choice", "year": 2025, "director": "Park Chan-wook", "cast": "Lee Byung-hun, Son Ye-jin, Park Hee-soon", "platform": "Neon / CJ Entertainment", "desc": "Безупречный сотрудник бумажной фабрики теряет работу — и решает «устранить» конкурентов на рынке труда буквально. Чан Ук снимает чёрную комедию о капитализме и отчаянии. Венеция 2025.", "imdb": "https://www.imdb.com/title/tt28835025/", "kp": "https://www.kinopoisk.ru/film/5440001/"}, {"title": "One Battle After Another", "year": 2025, "director": "Paul Thomas Anderson", "cast": "Leonardo DiCaprio, Sean Penn, Chase Infiniti", "platform": "Warner Bros.", "desc": "Выживший из 70-х снова встречается с прошлым, когда его дочь исчезает. PTA в лучшей форме, на плёнке VistaVision. Оскар за лучший фильм.", "imdb": "https://www.imdb.com/title/tt32469864/", "kp": "https://www.kinopoisk.ru/film/5369004/", "star": True}, {"title": "Rental Family", "year": 2025, "director": "Hikari", "cast": "Brendan Fraser, Takehiro Hira, Mari Yamamoto", "platform": "Searchlight Pictures", "desc": "Американский актёр в Токио без работы и смысла находит занятие: он играет «арендованного» родственника для незнакомцев. Постепенно эти чужие связи становятся единственными настоящими. TIFF 2025.", "imdb": "https://www.imdb.com/title/tt28835559/", "kp": "https://www.kinopoisk.ru/film/5369005/"}, {"title": "Resurrection", "year": 2025, "director": "Bi Gan", "cast": "—", "platform": "MUBI", "desc": "Третий фильм китайского режиссёра «Долгий день уходит в ночь»: шесть новелл, столетие китайской истории, шесть человеческих чувств — кино как медитация о памяти и времени. Каннский МКФ 2025.", "imdb": "https://www.imdb.com/title/tt30000002/", "kp": "https://www.kinopoisk.ru/film/5452000/"}, {"title": "Sentimental Value", "year": 2025, "director": "Joachim Trier", "cast": "Renate Reinsve, Stellan Skarsgård, Elle Fanning", "platform": "Neon", "desc": "Две сестры воссоединяются с отцом-режиссёром после смерти матери. Grand Prix Каннского МКФ.", "imdb": "https://www.imdb.com/title/tt28241249/", "kp": "https://www.kinopoisk.ru/film/5369006/"}, {"title": "Sinners", "year": 2025, "director": "Ryan Coogler", "cast": "Michael B. Jordan, Hailee Steinfeld, Jack O'Connell", "platform": "Warner Bros.", "desc": "Миссисипи, 1932: братья-близнецы открывают джук-джойнт — и первой же ночью туда приходит нечто древнее. 16 номинаций на Оскар — рекорд.", "imdb": "https://www.imdb.com/title/tt31193180/", "kp": "https://www.kinopoisk.ru/film/5369007/", "star": True}, {"title": "Sorry, Baby", "year": 2025, "director": "Eva Victor", "cast": "Eva Victor, Naomi Ackie, Louis Cancelmi", "platform": "A24", "desc": "Молодой профессор после сексуального насилия — не драма о травме, а исследование того, как жизнь продолжается рядом с ней.", "imdb": "https://www.imdb.com/title/tt28827001/", "kp": "https://www.kinopoisk.ru/film/5430002/"}, {"title": "Sound of Falling", "year": 2025, "director": "Mascha Schilinski", "cast": "Hanna Heckt, Lena Urzendowsky", "platform": "MUBI", "desc": "Четыре поколения женщин на немецкой ферме — сто лет одной семьи. Приз жюри Каннского МКФ. Открытие года.", "imdb": "https://www.imdb.com/title/tt28241250/", "kp": "https://www.kinopoisk.ru/film/5369008/"}, {"title": "The Phoenician Scheme", "year": 2025, "director": "Wes Anderson", "cast": "Benicio del Toro, Michael Cera, Scarlett Johansson", "platform": "Focus Features", "desc": "Умирающий магнат пытается передать бизнес-империю в надёжные руки. Андерсон снимает фарс о деньгах и родстве.", "imdb": "https://www.imdb.com/title/tt28363361/", "kp": "https://www.kinopoisk.ru/film/5400201/"}, {"title": "The Secret Agent", "year": 2025, "director": "Kleber Mendonça Filho", "cast": "Wagner Moura", "platform": "Neon", "desc": "Бразилия, 1977: разыскиваемый активист пытается вывезти сына из страны при военной диктатуре. Приз за режиссуру в Каннах.", "imdb": "https://www.imdb.com/title/tt27000000/", "kp": "https://www.kinopoisk.ru/film/5450000/"}, {"title": "Warfare", "year": 2025, "director": "Alex Garland, Ray Mendoza", "cast": "D'Pharaoh Woon-A-Tai, Will Poulter, Joseph Quinn", "platform": "A24", "desc": "Ирак, 2006: отряд Navy SEAL застрял под огнём. Без пафоса, без героизма — только реальное время и реальный ужас.", "imdb": "https://www.imdb.com/title/tt28826999/", "kp": "https://www.kinopoisk.ru/film/5253001/"}, {"title": "All We Imagine as Light", "year": 2024, "director": "Payal Kapadia", "cast": "Kani Kusruti, Divya Prabha, Chhaya Kadam", "platform": "MUBI", "desc": "Две медсестры в Мумбаи — и их тихие желания, одиночество и нежность. Grand Prix Канн.", "imdb": "https://www.imdb.com/title/tt28241248/", "kp": "https://www.kinopoisk.ru/film/5258001/"}, {"title": "Am I OK?", "year": 2024, "director": "Tig Notaro, Stephanie Allynne", "cast": "Dakota Johnson, Sonoya Mizuno, Jermaine Fowler", "platform": "Max / Gloria Sanchez", "desc": "Подруги детства: одна уезжает в Лондон, другая наконец признаётся ей — и себе — что никогда не была влюблена в мужчину. Нежная и смешная история камин-аута в 30 лет.", "imdb": "https://www.imdb.com/title/tt14882926/", "kp": "https://www.kinopoisk.ru/film/5241000/"}, {"title": "Challengers", "year": 2024, "director": "Luca Guadagnino", "cast": "Zendaya, Josh O'Connor, Mike Faist", "platform": "MGM / Amazon", "desc": "Теннисный турнир, любовный треугольник, и три человека, которые разрушили друг друга. Самый сексуальный фильм года.", "imdb": "https://www.imdb.com/title/tt16426838/", "kp": "https://www.kinopoisk.ru/film/5119702/"}, {"title": "Civil War", "year": 2024, "director": "Alex Garland", "cast": "Kirsten Dunst, Wagner Moura, Cailee Spaeny", "platform": "A24", "desc": "Недалёкое будущее: США в состоянии гражданской войны. Группа журналистов едет брать интервью у президента в осаждённом Вашингтоне. Не про политику — про цену взгляда.", "imdb": "https://www.imdb.com/title/tt17279496/", "kp": "https://www.kinopoisk.ru/film/5119703/"}, {"title": "Conclave", "year": 2024, "director": "Edward Berger", "cast": "Ralph Fiennes, Stanley Tucci, Isabella Rossellini", "platform": "Focus Features", "desc": "Кардинал расследует скандал внутри Ватикана во время выборов нового Папы. «Наследники» с кардиналами.", "imdb": "https://www.imdb.com/title/tt23561236/", "kp": "https://www.kinopoisk.ru/film/5253002/"}, {"title": "Daddio", "year": 2024, "director": "Christy Hall", "cast": "Dakota Johnson, Sean Penn", "platform": "Sony Pictures Classics", "desc": "Женщина едет на такси с JFK до дома — и за полтора часа случайный разговор с водителем переворачивает что-то внутри. Камерная история о любви, измене и честности. Дебют режиссёра.", "imdb": "https://www.imdb.com/title/tt26915282/", "kp": "https://www.kinopoisk.ru/film/5253003/"}, {"title": "Dune: Part Two", "year": 2024, "director": "Denis Villeneuve", "cast": "Timothée Chalamet, Zendaya, Austin Butler", "platform": "Warner Bros.", "desc": "Пол Атрейдес становится мессией фрименов — и цена этого пути оказывается выше, чем он думал.", "imdb": "https://www.imdb.com/title/tt15239678/", "kp": "https://www.kinopoisk.ru/film/4936991/"}, {"title": "Furiosa: A Mad Max Saga", "year": 2024, "director": "George Miller", "cast": "Anya Taylor-Joy, Chris Hemsworth, Tom Burke", "platform": "Warner Bros.", "desc": "Происхождение Фуриозы: от зелёного рая до выжженной пустыни — и путь женщины, превратившейся в легенду. Эпическая история мести длиной в десятилетие.", "imdb": "https://www.imdb.com/title/tt12037194/", "kp": "https://www.kinopoisk.ru/film/4936990/"}, {"title": "Ghostlight", "year": 2024, "director": "Kelly O'Sullivan, Alex Thompson", "cast": "Keith Kupferer, Dolly de Leon, Katherine Mallen Kupferer", "platform": "IFC Films", "desc": "Хмурый строитель случайно попадает в местную театральную постановку «Ромео и Джульетты» — и спектакль начинает зеркалить его собственную боль. 99% на RT, фильм года по версии National Board of Review.", "imdb": "https://www.imdb.com/title/tt28607952/", "kp": "https://www.kinopoisk.ru/film/5258002/"}, {"title": "I'm Still Here", "year": 2024, "director": "Walter Salles", "cast": "Fernanda Torres, Selton Mello", "platform": "Sony Pictures Classics", "desc": "Бразилия, 1971: муж исчезает после ареста. Жена решает не молчать — всю оставшуюся жизнь. Оскар за лучший международный фильм.", "imdb": "https://www.imdb.com/title/tt23849756/", "kp": "https://www.kinopoisk.ru/film/5253004/"}, {"title": "A Real Pain", "year": 2024, "director": "Jesse Eisenberg", "cast": "Jesse Eisenberg, Kieran Culkin", "platform": "Searchlight", "desc": "Два двоюродных брата едут в Польшу чтить память бабушки — и заново узнают, кто они такие. Оскар за лучшую мужскую роль второго плана.", "imdb": "https://www.imdb.com/title/tt23561235/", "kp": "https://www.kinopoisk.ru/film/5258003/"}, {"title": "September 5", "year": 2024, "director": "Tim Fehlbaum", "cast": "Peter Sarsgaard, Ben Chaplin, Leonie Benesch", "platform": "Paramount", "desc": "Команда ABC Sports случайно оказывается первой, освещающей теракт на Олимпиаде 1972 года — в прямом эфире.", "imdb": "https://www.imdb.com/title/tt23561237/", "kp": "https://www.kinopoisk.ru/film/5258004/"}, {"title": "Sirat", "year": 2024, "director": "Oliver Laxe", "cast": "—", "platform": "MUBI", "desc": "Группа людей пересекает Сахару, чтобы добраться до рейва. Экстаз, красота и конец света. Каннский МКФ 2024.", "imdb": "https://www.imdb.com/title/tt32002210/", "kp": "https://www.kinopoisk.ru/index.php?kp_query=Sirat+2024"}, {"title": "The Room Next Door", "year": 2024, "director": "Pedro Almodóvar", "cast": "Julianne Moore, Tilda Swinton, John Turturro", "platform": "Sony Pictures Classics", "desc": "Две давние подруги воссоединяются: одна умирает, другая соглашается быть рядом. Первый англоязычный фильм Альмодовара — Золотой лев Венеции.", "imdb": "https://www.imdb.com/title/tt23561238/", "kp": "https://www.kinopoisk.ru/film/5258005/"}, {"title": "The Substance", "year": 2024, "director": "Coralie Fargeat", "cast": "Demi Moore, Margaret Qualley, Dennis Quaid", "platform": "MUBI", "desc": "Стареющая звезда вводит препарат и порождает молодую версию себя. Боди-хоррор о женском теле как продукте. Оскар за сценарий.", "imdb": "https://www.imdb.com/title/tt17526714/", "kp": "https://www.kinopoisk.ru/film/5119704/"}, {"title": "Woman of the Hour", "year": 2024, "director": "Anna Kendrick", "cast": "Anna Kendrick, Daniel Zovatto, Tony Hale", "platform": "Netflix", "desc": "Режиссёрский дебют Анны Кендрик: Лос-Анджелес, 1978 — участница шоу «Игра в свидания» выбирает обаятельного холостяка, который оказывается серийным убийцей. Основано на реальной истории.", "imdb": "https://www.imdb.com/title/tt12286230/", "kp": "https://www.kinopoisk.ru/film/5258000/"}]},
}

# Load remaining results from the HTML file at runtime
import re, subprocess, tempfile, os as _os

def _load_all_results():
    try:
        html_path = _os.path.join(_os.path.dirname(__file__), 'quiz_bot.html')
        if not _os.path.exists(html_path):
            return RESULTS
        with open(html_path, 'r') as f:
            html = f.read()
        s = html.find('const results = {')
        if s == -1:
            return RESULTS
        depth = 0
        i = s + len('const results = ')
        end = -1
        for j in range(i, len(html)):
            if html[j] == '{': depth += 1
            elif html[j] == '}':
                depth -= 1
                if depth == 0: end = j; break
        rjs = html[s + len('const results = '):end+1]
        script = f"var r={rjs}; process.stdout.write(JSON.stringify(r));"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script)
            tmp = f.name
        res = subprocess.run(['node', tmp], capture_output=True, text=True, timeout=10)
        _os.unlink(tmp)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            return {int(k): v for k, v in data.items()}
    except Exception as e:
        logger.warning(f"Could not load results from html: {e}")
    return RESULTS

# ─── Quiz flow ────────────────────────────────────────────────────────────────
STEPS = {
    'welcome': {
        'text': (
            "👋 Привет\\! Я — *Лиса Астахова*, сценарист и продюсер, и это мой бот, который наконец подскажет, что посмотреть прямо сейчас\\.\n\n"
            "Это не бесконечные списки «великого»\\. Все фильмы и сериалы вышли в последние три года и отобраны лично мной\\.\n\n"
            "_Списки постоянно обновляются\\._"
        ),
        'buttons': [('Начать →', 'step1')]
    },
    'step1': {
        'text': '*Что смотрим сегодня?*',
        'buttons': [('🎬 Кино', 'step2'), ('📺 Сериал', 'step5'), ('🎞 Документалка', 'step8')]
    },
    'step2': {
        'text': '*Кино\\. Как выбираем?*',
        'buttons': [('По жанру', 'step3'), ('По настроению', 'step4'), ('По Лисе', 'r:9'), ('← назад', 'step1')]
    },
    'step3': {
        'text': '*Теперь жанр:*',
        'buttons': [('Драма', 'r:1'), ('Комедия', 'r:2'), ('Триллер / Хоррор', 'r:3'), ('← назад', 'step2')]
    },
    'step4': {
        'text': '*Какое настроение сейчас?*',
        'buttons': [
            ('Похмелье', 'r:4'), ('Романтичное', 'r:5'),
            ('Депрессивное и хочется хуже', 'r:6'),
            ('Депрессивное и хочется лучше', 'r:7'),
            ('Неожиданно весёлое', 'r:8'),
            ('← назад', 'step2')
        ]
    },
    'step5': {
        'text': '*Сериал\\. Как выбираем?*',
        'buttons': [('По жанру', 'step6'), ('По настроению', 'step7'), ('По Лисе', 'r:17'), ('← назад', 'step1')]
    },
    'step6': {
        'text': '*Выбираем жанр сериала:*',
        'buttons': [('Драма / Детектив', 'r:10'), ('Комедия', 'r:11'), ('← назад', 'step5')]
    },
    'step7': {
        'text': '*Какое настроение сейчас?*',
        'buttons': [
            ('Похмелье', 'r:12'),
            ('Депрессивное и хочется хуже', 'r:14'),
            ('Депрессивное и хочется лучше', 'r:15'),
            ('Неожиданно весёлое', 'r:16'),
            ('← назад', 'step5')
        ]
    },
    'step8': {
        'text': '*Документалка\\. В каком формате?*',
        'buttons': [('Полный метр', 'r:18'), ('Сериал', 'r:19'), ('← назад', 'step1')]
    },
}

PAGE_SIZE = 5  # films per page

# ─── Helpers ─────────────────────────────────────────────────────────────────
def escape_md(text: str) -> str:
    """Escape special characters for MarkdownV2."""
    special = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in special else c for c in str(text))

def format_film(f: dict) -> str:
    star = "⭐ " if f.get('star') else ""
    title = escape_md(f['title'])
    year = escape_md(str(f['year']))
    director = escape_md(f.get('director', ''))
    cast = escape_md(f.get('cast', ''))
    platform = escape_md(f.get('platform', ''))
    desc = escape_md(f.get('desc', ''))
    imdb = f.get('imdb', '')
    kp = f.get('kp', '')

    lines = [f"{star}*{title}* \\({year}\\)"]
    if director and director != '—':
        lines.append(f"реж\\. {director}")
    if cast and cast != '—':
        lines.append(f"_{cast}_")
    if platform and platform != '—':
        lines.append(platform)
    if desc:
        lines.append(f"\n{desc}")
    links = []
    if imdb:
        links.append(f"[IMDB]({imdb})")
    if kp:
        links.append(f"[Кинопоиск]({kp})")
    if links:
        lines.append(" · ".join(links))
    return "\n".join(lines)

def make_step_keyboard(buttons: list) -> InlineKeyboardMarkup:
    kb = []
    for label, cb in buttons:
        kb.append([InlineKeyboardButton(label, callback_data=cb)])
    return InlineKeyboardMarkup(kb)

def make_result_keyboard(result_id: int, page: int, total: int, from_step: str) -> InlineKeyboardMarkup:
    kb = []
    row = []
    if page > 0:
        row.append(InlineKeyboardButton("← Назад", callback_data=f"page:{result_id}:{page-1}:{from_step}"))
    if (page + 1) * PAGE_SIZE < total:
        row.append(InlineKeyboardButton("Ещё →", callback_data=f"page:{result_id}:{page+1}:{from_step}"))
    if row:
        kb.append(row)
    kb.append([InlineKeyboardButton("🔄 Начать заново", callback_data="welcome")])
    return InlineKeyboardMarkup(kb)

# ─── Handlers ─────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data.setdefault('results', _load_all_results())
    step = STEPS['welcome']
    await update.message.reply_text(
        step['text'],
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=make_step_keyboard(step['buttons'])
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    context.bot_data.setdefault('results', _load_all_results())
    all_results = context.bot_data['results']

    # ── Pagination ─────────────────────────────────────────────────────────
    if data.startswith('page:'):
        _, rid, pg, from_step = data.split(':')
        rid, pg = int(rid), int(pg)
        await show_result_page(query, all_results, rid, pg, from_step)
        return

    # ── Result ────────────────────────────────────────────────────────────
    if data.startswith('r:'):
        rid = int(data[2:])
        # Determine which step to go back to
        from_step = _find_from_step(rid)
        await show_result_page(query, all_results, rid, 0, from_step)
        return

    # ── Step ──────────────────────────────────────────────────────────────
    if data in STEPS:
        step = STEPS[data]
        await query.edit_message_text(
            step['text'],
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=make_step_keyboard(step['buttons'])
        )
        return

    # ── welcome shortcut ──────────────────────────────────────────────────
    if data == 'welcome':
        step = STEPS['step1']
        await query.edit_message_text(
            step['text'],
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=make_step_keyboard(step['buttons'])
        )

def _find_from_step(result_id: int) -> str:
    mapping = {
        1: 'step3', 2: 'step3', 3: 'step3',
        4: 'step4', 5: 'step4', 6: 'step4', 7: 'step4', 8: 'step4',
        9: 'step2',
        10: 'step6', 11: 'step6',
        12: 'step7', 14: 'step7', 15: 'step7', 16: 'step7',
        17: 'step5',
        18: 'step8', 19: 'step8',
    }
    return mapping.get(result_id, 'step1')

async def show_result_page(query, all_results: dict, rid: int, page: int, from_step: str):
    result = all_results.get(rid, {})
    films = result.get('films', [])
    title = result.get('title', f'Список {rid}')
    total = len(films)

    if not films:
        await query.edit_message_text(
            f"*{escape_md(title)}*\n\n_Список пуст\\._",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Начать заново", callback_data="welcome")
            ]])
        )
        return

    start_i = page * PAGE_SIZE
    end_i = min(start_i + PAGE_SIZE, total)
    page_films = films[start_i:end_i]

    header = f"*{escape_md(title)}*\n_{escape_md(str(start_i+1))}–{escape_md(str(end_i))} из {escape_md(str(total))}_\n\n"
    body = "\n\n—\n\n".join(format_film(f) for f in page_films)
    text = header + body

    # Telegram limit is 4096 chars — truncate if needed
    if len(text) > 4000:
        text = text[:3990] + "\\.\\.\\.\\."

    kb = make_result_keyboard(rid, page, total, from_step)
    try:
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=kb,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error sending result: {e}")
        # Fallback without markdown
        await query.edit_message_text(
            f"{title} ({start_i+1}–{end_i} из {total})\n\n" +
            "\n\n".join(f["title"] + f" ({f['year']})\n{f.get('desc','')}" for f in page_films),
            reply_markup=kb
        )

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
