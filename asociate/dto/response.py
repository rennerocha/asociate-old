class ResponseSuccess:
    def __init__(self, value=None):
        self.value = value


class ResponseFailure:
    def __init__(self, failure):
        self.value = {
            "error": True,
            "type": failure.__class__.__name__,
            "message": "{}".format(failure),
        }

    def __bool__(self):
        return False
