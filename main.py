# Написать программу на Python, которая советует пользователю подходящие игры из Steam на основе ответов
# пользователя в опросе.
#
# Программа должна обеспечивать:
#
# Диалоговый интерфейс с пользователем. Система последовательно узнает об интересующих жанрах, катерогиях, платформах
# и т.д. (соответственно полям в csv файле).
# Например:
# Какой жанр игры вас интересует?
# >>> RPG, Adventure
# Какая категория?
# >>> # если пустая строка, то  пользователю это не очень важно
# ...
# Поиск в файле steam.csv названий подходящих пользователю игр
# Формирование отчета в виде файла
# Вход программы: Файл steam.csv
#
# Выход программы: Отчет в виде файла

def collect_list(out_list, in_list):
    for i in in_list:
        if i in out_list:
            pass
        else:
            out_list.append(i)


def answer_analiz(ans, list_of_ans):
    ans_list = []
    if ans.count(',') > 0:
        num_list = ans.split(',')
    elif genres_ans.count(';') > 0:
        num_list = ans.split(';')
    else:
        num_list = ans.split(' ')
    for i in num_list:
        if i == '':
            ans_list.append(i)
        else:
            ans_list.append(list_of_ans[int(i)])
    return ans_list


def print_csv_string(element, f_out):
    if isinstance(element,type([])):
        sout = ','.join(element)
        f_out.write(f'{sout}')
    elif isinstance(element, type({})):
        lout = []
        for i in element:
            s1 = ';'.join(element[i])
            lout.append(s1)
        sout = ','.join(lout)
        f_out.write(f'{sout}')


# список доступных игр в Steam
games_list = []

# список доступных жанров
genres_list = []
# список доступных платформ
platforms_list = []
# список доспутный категорий
categories_list = []
# список стим-тэгов
tags_list = []


# считывание базы данных Steam, при этом составляем списки доступных вариантов выбора (жанры, платформы, доп. оптиции)
filename = 'steam.csv'
f = open(filename, 'r', encoding='utf8')
header = f.readline().split(',')

while True:
    s = 'a'
    fullstring = ' '
    quotations = 0
    while s != '\n' and s != '':
        try:
            s = f.read(1)
            # для правильного составления списков и словарей необходимо исключить запятые,
            # содержащиеся в названиях компаний (в ковычках)
            if s == '"':
                quotations += 1
            if s == ',' and quotations % 2 != 0:
                # заменяем запятую на пробел, если она заперта в ковычках
                s = ' '
            fullstring += s
        except UnicodeDecodeError:
            pass

    if s == '':
        break

    game = fullstring.split(',')

    # в списке game могут быть части, в которых содержится более 1 элемента, перечисленных через ";"
    for i in range(len(game)):
        # if game[i].count(';') > 0:
        game[i] = game[i].split(';')

    game_info = dict(zip(header, game))

    # обновляем списки доступных жанров, категорий и т.д.
    collect_list(platforms_list, game_info['platforms'])
    collect_list(categories_list, game_info['categories'])
    collect_list(genres_list, game_info['genres'])
    collect_list(tags_list, game_info['steamspy_tags'])

    games_list.append(game_info)

f.close()

# Начинаем опрос пользователя
print(f'Какие жанры игр вам нравятся? \033[31m')
for i in range(len(genres_list)):
    print(f'{i} - {genres_list[i]}')
print('\033[0m')
genres_ans = input()

print(f'Выберите категорию игр? \033[31m')
for i in range(len(categories_list)):
    print(f'{i} - {categories_list[i]}')
print('\033[0m')
categories_ans = input()

print(f'На какой платформе собираетесь игрыть? \033[31m')
for i in range(len(platforms_list)):
    print(f'{i} - {platforms_list[i]}')
print('\033[0m')
platforms_ans = input()

print(f'Выберите дополнительные аттрибуты для поиска? \033[31m')
for i in range(len(tags_list)):
    print(f'{i} - {tags_list[i]}')
print('\033[0m')
tags_ans = input()

print(f'Укажите максимальную цену: ')
max_price = input()

print(f'Спасибо! Формируем список подходящих игр...')

# анализируем ответы
genres_ans = answer_analiz(genres_ans, genres_list)
categories_ans = answer_analiz(categories_ans, categories_list)
platforms_ans = answer_analiz(platforms_ans, platforms_list)
tags_ans = answer_analiz(tags_ans, tags_list)
if (len(max_price) == 0) or not max_price.isnumeric():
    max_price = -1
else:
    max_price = float(str(max_price))

print(f'Выбранные жанры = {genres_ans}')
print(f'Выбранные категории = {categories_ans}')
print(f'Выбранные платформы = {platforms_ans}')
print(f'Дополнительные опции = {tags_ans}')
print(f'Максиамльная цена =  {max_price}')

# ведем поиск подходящих игры по базе данных и формируем новый список в файле result.csv
# открываем файл
fout = open('results.csv', 'wt', encoding='utf8')
print_csv_string(header, fout)
games_count = 0
for game in games_list:
    good_game = True
    good_genre = True
    good_category = True
    good_platform = True
    good_additional = True
    good_price = True
    if len(genres_ans[0]) > 0:
        # есть желаемые жанры (ищем подходящие в genres, categories, steamspy_tags)
        good_genre = False
        for gen in genres_ans:
            # gen = genres_list[int(i)]
            if (gen in game['genres']) or (gen in game['categories']) or (gen in game['steamspy_tags']):
                good_genre = True
    else:
        # жанры не важны
        pass
    if len(categories_ans[0]) > 0:
        # есть желаемые категории (ищем подходящие в genres, categories, steamspy_tags)
        good_category = False
        for category in categories_ans:
            # category = categories_list[int(i)]
            if (category in game['genres']) or (category in game['categories']) or (category in game['steamspy_tags']):
                good_category = True
    else:
        # категории не важны
        pass
    if len(platforms_ans[0]) > 0:
        # есть желаемые платформы
        good_platform = False
        for platform in platforms_ans:
            # platform = platforms_list[int(i)]
            if platform in game['platforms']:
                good_platform = True
    else:
        # платформы не важны
        pass
    if len(tags_ans[0]) > 0:
        # есть дополнительные желания
        good_additional = False
        for additional in tags_ans:
            # additional = tags_list[int(i)]
            if (additional in game['steamspy_tags']) or (additional in game['categories']):
                good_additional = True
    else:
        # дополнительные желания не важны
        pass
    if max_price >= 0:
        # есть максимальная допустимая цена
        good_price = False
        if max_price >= float(str(game['price\n'][0]).replace('\\n','')):
            good_price = True
    else:
        # цена не важна
        pass

    good_game = good_genre and good_category and good_additional and good_platform and good_price

    if good_game:
        # записываем в файл
        print_csv_string(game, fout)
        games_count += 1


print(f'Результаты с подходящими играми ({games_count} шт.) записыны в файл results.csv')