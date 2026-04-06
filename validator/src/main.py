from parser.schema_parser import SchemaParser
from parser.data_parser import DataParser
from validator.validator import Validator
from exceptions.custom_exceptions import AppError

def main():
    try:
        # Читаємо файли
        try:
            with open("../../schema.def") as f:
                schema_text = f.read()
        # Перевірки та вивід інформації в консоль
        except FileNotFoundError:
            print("Помилка: Файл 'schema.def' не знайдено")
            return
        except IOError as e:
            print(f"Помилка при читанні 'schema.def': {str(e)}")
            return

        # Відкриття файлу користувача
        try:
            with open("../../data.txt") as f:
                data_text = f.read()
        # Обробка дій
        except FileNotFoundError:
            print("Помилка: Файл 'data.txt' не знайдено")
            return
        except IOError as e:
            print(f"Помилка при читанні 'data.txt': {str(e)}")
            return

        # Парсимо схему та дані
        schema = SchemaParser().parse(schema_text)
        data = DataParser().parse(data_text)

        # Валідація даних
        validator = Validator(schema["User"])
        validator.validate(data)

        print("Валідація пройдена успішно!")

    # Обробка
    except AppError as e:
        print(f"Помилка валідації: {str(e)}")
        return
    except Exception as e:
        print(f"Неочікувана помилка: {str(e)}")
        return

if __name__ == "__main__":
    main()