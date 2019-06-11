from ._core import IogasXMLObject
from ..util.xml import prettify_xml
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class Diagram(IogasXMLObject):
    def __init__(self, *args, name="", xmlelement=None, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, **kwargs)

    def export(self, filename, encoding="utf-8", method="xml"):
        et = pyogas2xml(self)
        ElementTree(et).write(filename, method=method, encoding=encoding)
        return prettify_xml(et)


class FreeXYDiagram(Diagram):
    def __init__(self, *args, name="", xmlelement=None, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name))


class GeochemXYDiagram(Diagram):
    def __init__(self, *args, name="", xmlelement=None, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name))


class FreeTernaryDiagram(Diagram):
    def __init__(self, *args, name="", xmlelement=None, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name))
