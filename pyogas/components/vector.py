from ._core import IogasXMLObject
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class Linear(IogasXMLObject):
    def __init__(self, *args, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)


class Boundary3(IogasXMLObject):
    def __init__(self, *args, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)


class Boundary(IogasXMLObject):
    def __init__(self, *args, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)


class Bounds(IogasXMLObject):
    def __init__(self, *args, x=0.0, y=0.0, w=0.0, h=0.0, xmlelement=None, **kwargs):
        super().__init__(*args, xmlelement=xmlelement, **kwargs)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

    def to_xml(self):
        return self._to_xml(
            x=self.fltfmt.format(self.x),
            y=self.fltfmt.format(self.y),
            w=self.fltfmt.format(self.w),
            h=self.fltfmt.format(self.h),
        )


class RegionPolygon(IogasXMLObject):
    def __init__(self, *args, name="", visible=True, xmlelement=None, **kwargs):
        super().__init__(name=name, visible=visible, xmlelement=xmlelement, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name), visible=str(self.visible).lower())


class Poly(IogasXMLObject):
    def __init__(
        self,
        *args,
        name="",
        function="",
        visible=True,
        closed=True,
        xmlelement=None,
        **kwargs
    ):
        super().__init__(
            name=name, closed=closed, visible=visible, xmlelement=xmlelement, **kwargs
        )

    def to_xml(self):
        return self._to_xml(
            name=str(self.name),
            visible=str(self.visible).lower(),
            closed=str(self.closed).lower(),
        )


class Polygon(IogasXMLObject):
    def __init__(self, name="", *args, xmlelement=None, visible=True, **kwargs):
        super().__init__(name=name, xmlelement=xmlelement, visible=visible, **kwargs)

    def to_xml(self):
        return self._to_xml(name=str(self.name), visible=str(self.visible).lower())
