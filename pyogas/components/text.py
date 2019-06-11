from ._core import IogasXMLObject
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class Description(IogasXMLObject):
    def __init__(self, *args, name="", xmlelement=None, **kwargs):
        super().__init__(xmlelement=xmlelement, name=name, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name))


class TextField(IogasXMLObject):
    def __init__(self, *args, text=None, xmlelement=None, **kwargs):
        super().__init__(xmlelement=xmlelement, text=text or "", **kwargs)


class Reference(TextField):
    def __init__(self, *args, text=None, xmlelement=None, **kwargs):
        super().__init__(xmlelement=xmlelement, text=text, **kwargs)


class Comment(TextField):
    def __init__(self, *args, text=None, xmlelement=None, **kwargs):
        super().__init__(xmlelement=xmlelement, text=text, **kwargs)

    def to_xml(self):
        return self._to_xml()


class LabelAngle(IogasXMLObject):
    def __init__(self, *args, angle=0.0, xmlelement=None, **kwargs):
        super().__init__(xmlelement=xmlelement, **kwargs)
        self.angle = float(angle)

    def to_xml(self):
        return self._to_xml(angle=self.fltfmt.format(self.angle))


class Label(IogasXMLObject):
    def __init__(
        self, *args, name="", x=0.0, y=0.0, visible=True, xmlelement=None, **kwargs
    ):
        super().__init__(xmlelement=xmlelement, **kwargs)
        self.name = name
        self.x = float(x)
        self.y = float(y)


class Colour(IogasXMLObject):
    def __init__(self, *args, r=255, g=255, b=255, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)
        self.color = int(r), int(g), int(b)

    def to_xml(self):
        r, g, b = [str(c) for c in self.color]
        return self._to_xml(r=r, g=g, b=b)
