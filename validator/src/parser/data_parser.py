from model.data_node import DataNode


class DataParser:
    def parse(self, text):
        lines = text.splitlines()
        root = None

        for line in lines:
            line = line.strip()

            if line.endswith("{"):
                type_name = line.replace("{", "").strip()
                root = DataNode(type_name)

            elif ":" in line:
                key, value = line.split(":")
                root.fields[key.strip()] = value.strip()

        return root