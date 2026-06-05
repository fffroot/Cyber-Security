from argparse import ArgumentParser
from pathlib import Path
from itertools import cycle

parser = ArgumentParser(
    prog='xor_cipher_tool',
)


parser.add_argument("-i", "--input", help="Путь к входному файлу", required=True)
parser.add_argument("-k", "--key", help=" Ключ для XOR",type=str, required=True)
parser.add_argument("-o", "--output", help="Путь к выходному файлу (опциональный)")
parser.add_argument("-a", "--action", choices=["encrypt", "decrypt"],required=True)

args = parser.parse_args()


if not Path(args.input).is_file():
    parser.error(f"Файл не найден: {args.input}")

def xor_cipher(data: bytes ,key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    result = []
    for data_byte, key_byte in zip(data, cycle(key_bytes)):
        xored_byte = data_byte ^ key_byte
        result.append(xored_byte)
    return bytes(result)






if __name__ == "__main__":
    with open(args.input, 'rb') as f:
        data = f.read()
    result = xor_cipher(data, args.key)

    if args.output:
        with open(args.output, 'wb') as f:
            f.write(result)
        print(f"✅ Результат сохранен в {args.output}")
    else:
        safe_output = result.hex()
        print(safe_output)









