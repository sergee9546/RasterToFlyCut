Simple utility to convert raster images into G-code optimized to FlyCut strategy of laser cutting.

Installation:

pip install PIL

How to use:
add a path to your image file into a variable "PathToFile".
Run script, file with extension ".lcc" appears.

Простая утилита для перевода растровой графики в G код для 
лазерных станков с чпу, оптимизированный для использования с
технологией резки "на лету".

Установите пакет PIL

pip install PIL

Как пользоватся:
Пропишите путь к файлу в переменную "PathToFile"
Запустите скрипт. Появится файл с расширением "llc".
Затащите его в управляющую программу. Если используете
CypCut, переименуйте расширение на ".nc"