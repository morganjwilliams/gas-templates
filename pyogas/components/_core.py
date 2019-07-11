from xml.etree.ElementTree import ElementTree, Element, parse

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class IogasXMLObject(object):
    fltfmt = "{:f}"  # arbitrary precision floats

    def __init__(
        self,
        *args,
        name=None,
        xmlelement=None,
        visible=None,
        closed=None,
        text=None,
        children=[],
        **kwargs
    ):
        self.xmlelement = xmlelement
        self.children = children

        if name is not None:
            self.name = name

        # visual, polygon elements
        if visible is not None:
            self.visible = str(visible).upper() == "TRUE"

        if closed is not None:
            self.closed = str(closed).upper() == "TRUE"

        if text is not None:
            self.text = text

        if self.xmlelement is not None:
            # iter parse
            self._parse_from_element()

    def _parse_from_element(self):
        for child in self.xmlelement:
            self.children.append(xml2pyogas(child))

    def _to_xml(self, **kwargs):
        if self.xmlelement is not None:
            return self.xmlelement
        else:
            # TODO: have some automated way to export elements
            el = Element(self.__class__.__name__, **kwargs)
            if hasattr(self, "text"):
                el.text = self.text
            return el

    def to_xml(self):
        return self._to_xml()
