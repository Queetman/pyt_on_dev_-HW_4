# -*- coding: utf-8 -*-
"""web_scrapping_hw.ipynb"

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vrOmhJWUTj4r0nRCRK0Bl_m486YsileQ

Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по ссылке
Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.

Ссылка: https://spb.hh.ru/search/vacancy?text=python&area=1&area=2
"""

import bs4
import requests

!pip install fake_headers # библиотека для созадния фейковых хедеров.

from fake_headers import Headers

def get_fake_headers():
  return Headers(browser = 'chrome', os = 'win').generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers =get_fake_headers())

response.request.headers # сейчас с браузера

# поиски
# 1)Pyton -название вакансии.
# 2) Город - Москва и Спб
# 3) провалисть в описание вакансии и там найти jango и flask

main_page_data = bs4.BeautifulSoup(response.text,  features = 'lxml') # Здесь хранится весть текст страницы

# Сначала нужно найти описание вакансий

#'bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-8 bloko-column_l-12'

names_data =main_page_data.findAll('span', class_ = 'vacancy-name--SYbxrgpHgHedVTkgI_cA serp-item__title-link serp-item__title-link_redesign')
len(names)# 20 статей на станице

# название вакансий
names =[]

for name in names_data:
  names.append(name.text)



pprint(names)

# 2) Город - Москва и Спб
#зашито глубоко ниже по уровням
#<span class="fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj">Москва</span>

#class = serp-item-control-xs-only--TtEuxuHSINMBcyYiTHf_
#<span class="fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj">Москва</span></span>

cities =main_page_data.findAll('span', class_ = 'fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj')

import re

city_list =[]

for city in cities:
  print(city.text)

import re

city_list =[]
# удаляем строки с цифрами в тектсе.
for city in cities:
  if re.search('\d+', city.text) is not None:
    pass
  else:
    city_list.append(city.text)

city_list

print(len(city_list))# значения задвоены. Нужно вывести каждое второе значение

city_list= [city_list[i] for i in range(1, len(city_list), 2)]
pprint(city_list)

len(city_list)

#Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".

# Сначала нужно получить ссылки на эти вакансии
bloko_links = main_page_data.findAll(class_="serp-item__title-link-wrapper", )

bloko_links

# получене тэгов со ссылками и списка ссылок
links = []

for bloko_link in bloko_links:
  if  bloko_link is not None:
    tag = bloko_link.find(class_="bloko-link")
    links.append(tag['href'])
    print(tag)

pprint(links)

# Сcылки есть. Теперь необходимо получить описание каждой вакансии

#bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-10
#g-user-content

#сделаем сначала для одной ссылки

response = requests.get(links[0], headers =get_fake_headers())
vacancy_data = bs4.BeautifulSoup(response.text,  features = 'lxml') # Здесь хранится весть текст страницы

#class_ = 'bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-10'

description  =vacancy_data.find(class_ = 'g-user-content')

description.text # Описание получено.

#Для всех ссылок вакансий

descriptions =[]

for link in links:
  response = requests.get(link, headers =get_fake_headers())
  vacancy_data = bs4.BeautifulSoup(response.text,  features = 'lxml') # Здесь хранится весть текст страницы
  descriptions.append(vacancy_data.find(class_ = 'g-user-content').text)

len(descriptions)

descriptions

#нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask"  и сохранить в json файл
search = ["Django", "Flask"]
data = [names, city_list, descriptions]
filt_data =[]
parsed_data =[]

for i in range(len(names)):
  for s in search:
    if s  in data[2][i]:
      filt_data.append([names[i], city_list[i], descriptions[i]])
      parsed_data.append({
    'names': names[i],
    'city_list': city_list[i],
    'descriptions': descriptions[i],
   })

parsed_data

# запись в json
import json

with open('hw_parsing.json', 'w') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))