from ._core import IogasXMLObject
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class Point(IogasXMLObject):
    def __init__(self, *args, x=0.0, y=0.0, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)
        self.x = float(x)
        self.y = float(y)

    def to_xml(self):
        return self._to_xml(x=self.fltfmt.format(self.x), y=self.fltfmt.format(self.y))


class BezierPoint(IogasXMLObject):
    def __init__(
        self, *args, x=0.0, y=0.0, sectionEnd=False, xmlelement=None, **kwargs
    ):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)
        self.x = float(x)
        self.y = float(y)
        self.sectionEnd = str(sectionEnd).upper() == "TRUE"

    def to_xml(self):
        return self._to_xml(
            x=self.fltfmt.format(self.x),
            y=self.fltfmt.format(self.y),
            sectionEnd=str(self.sectionEnd).lower(),
        )


class TPoint(IogasXMLObject):
    def __init__(self, *args, a=0.0, b=0.0, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)
        self.a = float(a)
        self.b = float(b)

    def to_xml(self):
        return self._to_xml(a=self.fltfmt.format(self.a), b=self.fltfmt.format(self.b))


class PointFeature(IogasXMLObject):
    def __init__(
        self,
        *args,
        x=0.0,
        y=0.0,
        pixelRadius=5.0,
        visible=True,
        xmlelement=None,
        **kwargs
    ):
        super().__init__(*args, visible=visible, xmlelement=xmlelement, **kwargs)
        self.x = float(x)
        self.y = float(y)
        self.pixelRadius = float(pixelRadius)

    def to_xml(self):
        return self._to_xml(
            name=str(self.name),
            x=self.fltfmt.format(self.x),
            y=self.fltfmt.format(self.y),
            pixelRadius=self.fltfmt.format(self.pixelRadius),
            visible=str(self.visible).lower(),
        )


class LabelPos(IogasXMLObject):
    def __init__(
        self, *args, x=None, y=None, a=None, b=None, xmlelement=None, **kwargs
    ):
        super().__init__(xmlelement=xmlelement, **kwargs)
        if x is not None:
            self.x = float(x)
            self.y = float(y)
        if a is not None:
            self.a = float(a)
            self.b = float(b)

    def to_xml(self):
        if hasattr(self, "x"):  # cartesian mode
            return self._to_xml(
                x=self.fltfmt.format(self.x), y=self.fltfmt.format(self.y)
            )
        else:  # ternary mode
            return self._to_xml(
                a=self.fltfmt.format(self.a), b=self.fltfmt.format(self.b)
            )
