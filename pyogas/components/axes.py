from ._core import IogasXMLObject
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Axis(IogasXMLObject):
    def __init__(self, *args, name="", log=False, xmlelement=None, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, **kwargs)
        self.log = log

    def to_xml(self):
        return self._to_xml(name=str(self.name), log=str(self.log))


class FunctionAxis(Axis):
    def __init__(
        self, *args, name="", function="", log=False, xmlelement=None, **kwargs
    ):
        super().__init__(
            name=name, log=log, function="", xmlelement=xmlelement, **kwargs
        )
        self.function = function

    def to_xml(self):
        return self._to_xml(
            name=str(self.name), function=str(self.function), log=str(self.log)
        )


class FreeAxis(Axis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FreeAxisA(FreeAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FreeAxisB(FreeAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FreeAxisC(FreeAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FreeFunctionAxisX(FunctionAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FreeFunctionAxisY(FunctionAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GeochemFunctionAxisX(FunctionAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GeochemFunctionAxisY(FunctionAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
