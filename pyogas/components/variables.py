from ._core import IogasXMLObject
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Variable(IogasXMLObject):
    def __init__(
        self, *args, letter="", element="", unit="", xmlelement=None, **kwargs
    ):
        super().__init__(
            *args,
            letter=letter,
            element=element,
            unit=unit,
            xmlelement=xmlelement,
            **kwargs
        )
        self.letter = letter
        self.element = element
        self.unit = unit

    def to_xml(self):
        return self._to_xml(
            letter=str(self.letter), element=str(self.element), unit=str(self.unit)
        )


class FreeVariable(IogasXMLObject):
    def __init__(self, *args, letter="", columnName="", xmlelement=None, **kwargs):
        super().__init__(
            *args, letter=letter, columnName=columnName, xmlelement=xmlelement, **kwargs
        )
        self.letter = letter
        self.columnName = columnName

    def to_xml(self):
        return self._to_xml(letter=str(self.letter), columnName=str(self.columnName))
