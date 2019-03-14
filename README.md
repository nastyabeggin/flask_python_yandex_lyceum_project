---
title: Создание заметок к различным произведениям 
Бегинина А.А.
---
Этот проект был создан в качестве макета электронной библиотеки с возможностью добавления пометок к различным книгам. Он подойдет для школьников, так как там добавлены несколько произведений из школьной программы.

-Реализованы: 
-
	- вход, выход, регистрация с проверкой логина и возможностью запомнить пользователя
	- база данных, содержащая таблицы с пользователями, книгами, заметками
	- администраторы, которые могут просматривать и удалять все заметки, таблицу пользователей, добавлять и удалять книги и свои записи
	- пользователи, которые могут добавлять свои заметки и удалять их, просматривать только свои заметки, видеть список всех книг
	- добавлены 6 произведений с названием, автором, аннотацией, годом написания и изображением

-Использовались:
-
	- компоненты Bootstrap(таблицы, карточки, формы)
	- SQL для создания таблиц в бд
	- Flask & Flask-wtf
	- шаблоны, наследуемые от base.html c различными циклами и условиями
	- статический контент
	- json
