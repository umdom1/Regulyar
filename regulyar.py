
from pprint import pprint
import csv
import re
from collections import Counter


with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    new_contacts_list = []

    for el in contacts_list:
        dict_contact = {}
        dict_contact['lastname'] = el[0]
        dict_contact['firstname'] = el[1]
        dict_contact['surname'] = el[2]
        dict_contact['organization'] = el[3]
        dict_contact['position'] = el[4]
        dict_contact['phone'] = el[5]
        dict_contact['email'] = el[6]
        new_contacts_list.append(dict_contact)


    # Список первых слов
    lastname_list = []
    for el in new_contacts_list:
        lastname_el = el['lastname'].split()[0]
        lastname_list.append(lastname_el)

    # Считает по списку первых слов количество и сохраняет в список где больше 2-х
    double_list = []
    for k, v in Counter(lastname_list).items():
        if v > 1:
            double_list.append(k)

    # Проходит по двум спискам и сохраняет по ключу в словарь
    finish_list = []
    for ele in double_list:
        double_dict = []
        for el in new_contacts_list:
            if ele == el['lastname'] or ele == str(el['lastname']).split()[0]:
                double_dict.append(el)
        double_dict_2 = double_dict.copy()[0]
        for k, v in double_dict[1].items():
            if v != '':
                double_dict_2[k] = v
        finish_list.append(double_dict_2)



    # Добавляем в общий список
    indexes = []
    for ele in double_list:
        for el in new_contacts_list:
            if ele == el['lastname'] or ele == str(el['lastname']).split()[0]:
                indexes.append(new_contacts_list.index(el))
    for index in sorted(indexes, reverse=True):
        del new_contacts_list[index]

    new_contacts_list = new_contacts_list + finish_list

    del contacts_list[:]

    for el in new_contacts_list:
        el_list = []
        for key, values in el.items():
            el_list.append(values)
        contacts_list.append(el_list)



# Регулярные выражения
# Поиск ФИО и распределение по столбцам

    pattern = r"([А-Я][а-я]+[,]?\s?)"
    for el in contacts_list:
        res = list(re.finditer(pattern, str(el[0:3])))
        index = 0
        for ele in res:
            el[index] = ele.group().strip()
            index += 1

    #  Поиск и замена телефона

    contacts_list_finish = []

    pattern = r'[+]*([0-9])\s*[(]?([0-9]{3})[)]?[-]*\s*([0-9]{3})[-]*\s*([0-9]{2})[-]*\s*([0-9]{2})\s*[(]*(доб\.)*[)]*\s*([0-9]+)*[)]*'
    repl = r'+7(\2)\3\4\5 \6\7'
    for el in contacts_list:
        el_res = []
        for el_sub in el:
            res = re.sub(pattern, repl, el_sub)
            el_res.append(res)
        contacts_list_finish.append(el_res)



    # Загрузка в файл

with open("phonebook.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(contacts_list_finish)
