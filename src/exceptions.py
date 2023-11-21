class IncorrectArgumentUsage(Exception):
    def __init__(self, message="Incorrect argument usage, "
                               "use --help for more information."):
        self.message = message
        super().__init__(self.message)


class InvalidPortNumber(Exception):
    def __init__(self, message="Invalid port number, needs to be in the "
                               "range of 1 - 65535 (inclusive)"):
        self.message = message
        super().__init__(self.message)


class InvalidHostName(Exception):
    def __init__(self, message="Cannot resolve domains IP address"):
        self.message = message
        super().__init__(self.message)
