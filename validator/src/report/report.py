class ReportGenerator:
    def generate(self, result):
        if result.is_valid:
            print("Validation Passed")
        else:
            print("Validation Failed")
            for err in result.errors:
                print(err)