import hashlib
import os.path
from argparse import ArgumentParser
from pathlib import Path
import json



parser = ArgumentParser(
    prog="fim"
)


parser.add_argument("-a", "--action",choices=["init", "check"],required=True, help="accepts only two values: 'init' or 'check'")
parser.add_argument("-p", "--path", help="the path to the target directory", required=True)
parser.add_argument("-d", "--db", help="the path to the database file (for example, baseline.json)",required=True)
args = parser.parse_args()



def collect_files(path):
    path = Path(path)
    if not path.is_dir():
        raise ValueError(f"Указанный путь не является директорией: {path}")
    ab_path = []
    try:
        for file in path.rglob("*"):
            try:
                if file.is_file():
                    ab_path.append(file.resolve())
            except FileNotFoundError:
                print(f"⚠️ Файл исчез: {file}")
                continue
            except PermissionError:
                print(f"Нет доступа к {file}")
                continue
    except PermissionError:
        print(f"Нет доступа к {path}")
    return ab_path





def calculate_file_hash(file_path: Path) -> str:
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                hash_obj.update(chunk)
    except PermissionError:
        print(f"Нет доступа к {file_path}")
        return None
    except IsADirectoryError as e:
        print(f"Ошибка: {e}")
        return None
    return hash_obj.hexdigest()

def get_file_info(directory_path: Path, db_path: Path) -> dict:
    baseline = {}
    path_files = collect_files(directory_path)
    if not path_files:
        print("Не удалось просканировать директорию")
    for file in path_files:
        if file == db_path.resolve():
            continue
        file_hash = calculate_file_hash(file)
        if file_hash is None:
            continue
        file_stat = file.stat()
        baseline[str(file)] = {
            "hash": file_hash,
            "size": file_stat.st_size,
            "mtime": file_stat.st_mtime
        }
    return baseline


if args.action == 'init':
    print(f"🔍 Сканирование директории: {args.path}")
    baseline_data = get_file_info(Path(args.path), Path(args.db))

    # Сохранение в JSON
    with open(args.db, 'w', encoding='utf-8') as f:
        json.dump(baseline_data, f, indent=4)

    print(f"✅ База создана. Проиндексировано {len(baseline_data)} файлов в {args.db}")
elif args.action == 'check':
    print(f"🔍 Сканирование директории: {args.path}")
    if not Path(args.db).exists():
        print("❌ База не найдена. Сначала выполните: fim -a init -p <путь> -d <база>")
        exit(1)

    with open(args.db, 'r', encoding='utf-8') as f:
        baseline = json.load(f)
    current = get_file_info(Path(args.path), Path(args.db))
    added = set(current.keys()) - set(baseline.keys())
    deleted = set(baseline.keys()) - set(current.keys())
    common = set(baseline.keys()) & set(current.keys())
    print(f"Добавлено: {len(added)}")
    for f in added:
        print(f"   ➕ {f}")
    print(f"Удалено: {len(deleted)}")
    for f in deleted:
        print(f"   ➖ {f}")
    modified_files = []
    for path_file in common:
        if baseline[path_file] != current[path_file]:
            modified_files.append(path_file)
    print(f"Изменено: {len(modified_files)}")
    for f in modified_files:
        print(f"   ! {f}")








