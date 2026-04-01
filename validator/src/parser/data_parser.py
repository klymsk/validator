import re

class DataParser:
    def parse(self, text):
        text = re.sub(r'(\w+):', r'"\1":', text)
        text = text.replace("true", "True").replace("false", "False")

        # прибираємо типи типу User {
        text = re.sub(r'\w+\s*{', '{', text)

        return eval(text)


# import json
# from exceptions.custom_exceptions import ParserError

# class DataParser:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     def parse(self):
#         try:
#             with open(self.file_path, "r", encoding="utf-8") as f:
#                 return json.load(f)

#         except FileNotFoundError:
#             raise ParserError("Файл не знайдено")

#         except json.JSONDecodeError:
#             raise ParserError("Невірний формат JSON")
        
