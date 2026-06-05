# Multi-Format Encoder/Decoder

Универсальный CLI-инструмент для кодирования и декодирования данных в различных форматах. Поддерживает работу как с текстовыми, так и с бинарными файлами (изображения, шеллкоды, PDF и т.д.).

## 🚀 Возможности

- **4 формата кодирования:** Base64, Hex, URL-encoding, ROT13
- **Работа с любыми файлами:** Корректно обрабатывает бинарные данные (не только текст)
- **Гибкий вывод:** Результат можно вывести в терминал или сохранить в файл
- **Защита от ошибок:** Graceful handling невалидных данных при декодировании
- **Production-ready:** Чистая архитектура с маршрутизацией через словарь функций

## 📋 Требования

- Python 3.10+
- Только стандартные библиотеки Python (не требует установки зависимостей)

## 🛠 Установка

```bash
git clone https://github.com/fffroot/Cyber-Security.git
cd Cyber-Security/02_multi_format_encoder_decoder
```

## 💻 Использование

### Базовый синтаксис

```bash
python encoder.py -a {encode|decode} -f {base64|hex|url|rot13} -i <input_file> [-o <output_file>]
```

### Аргументы

| Аргумент | Описание | Обязательный |
|----------|----------|--------------|
| `-a, --action` | Действие: `encode` (кодировать) или `decode` (декодировать) | ✅ |
| `-f, --format` | Формат: `base64`, `hex`, `url`, `rot13` | ✅ |
| `-i, --input` | Путь к входному файлу | ✅ |
| `-o, --output` | Путь к выходному файлу (опционально) | ❌ |

### Примеры использования

#### Кодирование текста в Base64

```bash
echo "secret payload" > input.txt
python encoder.py -a encode -f base64 -i input.txt
# Вывод: c2VjcmV0IHBheWxvYWQK
```

#### Кодирование с сохранением в файл

```bash
python encoder.py -a encode -f hex -i payload.txt -o payload.hex
# ✅ Результат сохранен в payload.hex
```

#### Декодирование Base64

```bash
echo "c2VjcmV0IHBheWxvYWQK" > encoded.txt
python encoder.py -a decode -f base64 -i encoded.txt
# Вывод: secret payload
```

#### URL-encoding для веб-параметров

```bash
echo "user=admin&pass=123" > params.txt
python encoder.py -a encode -f url -i params.txt
# Вывод: user%3Dadmin%26pass%3D123
```

#### ROT13 (симметричное шифрование)

```bash
echo "hello world" > text.txt
python encoder.py -a encode -f rot13 -i text.txt
# Вывод: uryyb jbeyq

python encoder.py -a encode -f rot13 -i text.txt  # Декодирование = кодирование для ROT13
# Вывод: hello world
```

#### Работа с бинарными файлами

```bash
# Кодируем изображение в Base64
python encoder.py -a encode -f base64 -i image.jpg -o image.b64

# Кодируем шеллкод в Hex
python encoder.py -a encode -f hex -i shellcode.bin -o shellcode.hex
```

## 🔧 Архитектура

Инструмент использует **словарь функций (dispatch dictionary)** для маршрутизации запросов, что делает код легко расширяемым. Чтобы добавить новый формат, достаточно:

1. Написать функции `encode_<format>` и `decode_<format>`
2. Добавить их в словарь `router`

## 🛡️ Обработка ошибок

- **Невалидные данные при декодировании:** Скрипт выводит понятное сообщение об ошибке и завершается с кодом 1 (вместо падения с трейсбеком)
- **Бинарные файлы с текстовыми форматами:** При попытке применить URL-encoding или ROT13 к бинарному файлу скрипт корректно сообщает об ошибке декодирования UTF-8

## 📝 Лицензия

MIT

## 👤 Автор

[fffroot](https://github.com/fffroot)

## 🤝 Вклад в проект

Этот проект является частью обучающего репозитория [Cyber-Security](https://github.com/fffroot/Cyber-Security), где собраны инструменты для изучения информационной безопасности.



