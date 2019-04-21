
class InvalidCredentialsException:

    def __init__(self, message):
        self.message = message

    def toString(self):
        return self.message