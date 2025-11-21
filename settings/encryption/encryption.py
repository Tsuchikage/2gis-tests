import os
import pyAesCrypt

# ==== НАСТРОЙКИ ====
MODE = "encrypt"  # encrypt или decrypt
FILENAME = "dev-example.com.env"  # имя файла в папке configuration/
PASSWORD = "Example123"  # пароль
DELETE_SOURCE = False  # True - удалить исходный файл после действия

# ==== КОНСТАНТЫ ====
BUFFER_SIZE = 64 * 1024
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONFIG_DIR = os.path.join(BASE_DIR, "configuration")


def encrypt_file(filepath: str, password: str):
    input_path = filepath
    output_path = input_path + ".aes"

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Файл для шифрования не найден: {input_path}")

    pyAesCrypt.encryptFile(input_path, output_path, password, BUFFER_SIZE)
    print(f"Файл зашифрован: {output_path}")

    if DELETE_SOURCE:
        os.remove(input_path)
        print(f"Исходный файл удалён: {input_path}")


def decrypt_file(filepath: str, password: str):
    if not filepath.endswith(".aes"):
        raise ValueError("Файл для расшифровки должен иметь расширение .aes")

    input_path = filepath
    output_path = input_path.removesuffix(".aes")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Файл для расшифровки не найден: {input_path}")

    pyAesCrypt.decryptFile(input_path, output_path, password, BUFFER_SIZE)
    print(f"Файл расшифрован: {output_path}")

    if DELETE_SOURCE:
        os.remove(input_path)
        print(f"Зашифрованный файл удалён: {input_path}")


if __name__ == "__main__":
    target_path = os.path.join(CONFIG_DIR, FILENAME)

    if MODE == "encrypt":
        encrypt_file(target_path, PASSWORD)
    elif MODE == "decrypt":
        decrypt_file(target_path, PASSWORD)
    else:
        raise ValueError(f"Неверный режим. Используй 'encrypt' или 'decrypt'. Сейчас: {MODE}")
