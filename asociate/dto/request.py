class ValidRequestObject:
    ...

class InvalidRequestObject:
    def __init__(self):
        self.errors = []

    def __bool__(self):
        return False

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        return len(self.errors) > 0