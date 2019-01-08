class Error():
    user_message = ""
    internal_message = ""
    code = ""
    more_info = ""

    def __init__(self, user_message, internal_message, code, more_info):
        self.user_message = user_message
        self.internal_message = internal_message
        self.code = code
        self.more_info = more_info

    def to_json(self):
        return {
            'userMessage': self.user_message,
            'internalMessage': self.internal_message,
            'code': self.code,
            'more info': self.more_info
        }