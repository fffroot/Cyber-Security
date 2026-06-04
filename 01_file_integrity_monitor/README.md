# File Integrity Monitor (FIM)

Инструмент командной строки для мониторинга целостности файлов в заданной директории. Вычисляет SHA-256 хеши и отслеживает метаданные (размер, время модификации).

## Возможности
- Рекурсивный обход директорий с обработкой ошибок прав доступа.
- Оптимизированное чтение файлов чанками (без перегрузки RAM).
- Сравнение состояний: выявление добавленных, удаленных и измененных файлов.

## Использование

1. Инициализация базы (снимок состояния):
   ```bash
   python fim.py -a init -p /путь/к/директории -d baseline.json
   ```
2. Проверка изменений:
    ```bash
   python fim.py -a check -p /путь/к/директории -d baseline.json
   ```

### Тестовые данные
```bash
mkdir -p /tmp/fim_check_test
echo "original" > /tmp/fim_check_test/file1.txt
echo "to_delete" > /tmp/fim_check_test/file2.txt

python fim.py -a init -p /tmp/fim_check_test -d /tmp/fim_check_test/base.json

echo "modified" > /tmp/fim_check_test/file1.txt
rm /tmp/fim_check_test/file2.txt
touch /tmp/fim_check_test/file3.txt

python fim.py -a check -p /tmp/fim_check_test -d /tmp/fim_check_test/base.json
```
    