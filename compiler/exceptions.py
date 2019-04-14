
class TranslatorException(Exception):
    def __init__(self, message=None, line=None):
        msg = "RAISED ON LINE {},\n".format(line) if line else ""
        msg += "MESSAGE: {}".format(message) if message else "There is no message"
        super().__init__(msg)


class LexicException(TranslatorException):
    pass
class NotFoundLexemException(LexicException):
    pass
class NotFoundIdnException(NotFoundLexemException):
    pass
class NotFoundConException(NotFoundLexemException):
    pass


class SemanticException(TranslatorException):
    pass
class UndefinedVariableException(SemanticException):
    pass
class VariableRedeclarationException(SemanticException):
    pass


class NoEndOfProgramSymbolException(TranslatorException):
    pass

class SyntaxException(TranslatorException):
    pass

class BuildException(TranslatorException):
    pass