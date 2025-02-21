
class UserDefinedException(Exception):

    def __init__(self, message='', code=''):
        super(UserDefinedException, self).__init__()
        self.message = message
        self.code = code

    def __str__(self):
        return f'({self.message}, {self.code})'
        # return '({0.message!s},{0.code!s})'.format(self)


class FileFormatException(UserDefinedException):
    pass


class ReportFileException(UserDefinedException):
    pass


class ProjectNameException(UserDefinedException):
    pass


class TestrialException(UserDefinedException):
    pass


class YamlLoadException(UserDefinedException):
    pass


class JsonLoadException(UserDefinedException):
    pass


class FileNotFoundException(UserDefinedException):
    pass


class EnvVariablesException(UserDefinedException):
    pass


class GlsVariablesException(UserDefinedException):
    pass


class JSONParseException(UserDefinedException):
    pass


class SortTypeException(UserDefinedException):
    pass


class NoValidationTypeException(UserDefinedException):
    pass

def test_exception():
    result = UserDefinedException("error_information", "404")
    print(result)
    assert "404" in str(result)


# if __name__ == '__main__':
#     result = UserDefinedException("error_information", "404")
#     print(result)
#     print(type(result))
#     # assert "404" in result
