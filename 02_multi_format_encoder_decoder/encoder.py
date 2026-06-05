import base64
import codecs
from urllib import parse
from argparse import ArgumentParser
from pathlib import Path
import sys


parser = ArgumentParser(
    prog="fmt_encoder_decoder",
)


parser.add_argument("-a","--action",choices=["encode","decode"], required=True)
parser.add_argument("-f", "--format", choices=["base64", "hex", "url", "rot13"],required=True)
parser.add_argument("-i", "--input", help = "Путь к исходному файлу", required=True)
parser.add_argument("-o", "--output", help = "Путь к файлу для сохранения результата (опционально)")

args = parser.parse_args()

if not Path(args.input).exists():
    parser.error(f"Файл не найден: {args.input}")


def encode_base64(data: bytes) -> bytes:
    return base64.b64encode(data)

def decode_base64(data: bytes) -> bytes:
    try:
        return base64.b64decode(data)
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

def encode_hex(data: bytes) -> str:
    return data.hex()

def decode_hex(data: str) -> bytes:
    try:
        return bytes.fromhex(data)
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

def encode_url(data: str) -> str:
    return parse.quote(data)

def decode_url(data: str) -> str:
    return parse.unquote(data)

def encode_rot13(data: str) -> str:
    return codecs.encode(data, 'rot_13')

def decode_rot13(data: str) -> str:
    return codecs.decode(data, 'rot_13')


with open(args.input, 'rb') as f:
    raw_data = f.read()
    router = {
        "base64": {"encode": encode_base64, "decode": decode_base64},
        "hex": {"encode": encode_hex, "decode": decode_hex},
        "url": {"encode": encode_url, "decode": decode_url},
        "rot13": {"encode": encode_rot13, "decode": decode_rot13},
    }
    chosen_func = router[args.format][args.action]
    if args.format == "url" or args.format == "rot13":
        try:
            raw_data = raw_data.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Ошибка:{e}")
            sys.exit(1)

    result = chosen_func(raw_data)

    if isinstance(result, bytes):
        output_text = result.decode('ascii', errors='ignore')
    else:
        output_text = result

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"✅ Результат сохранен в {args.output}")
    else:
        print(output_text)





