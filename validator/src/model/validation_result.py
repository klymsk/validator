class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []

    def add_error(self, error):
        self.is_valid = False
        self.errors.append(error)