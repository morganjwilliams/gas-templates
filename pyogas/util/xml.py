from lxml import etree as ET
from xml.etree.ElementTree import Element
from xml.dom import minidom
import re


def prettify_xml(elem, encoding="utf-8"):
    """
    Return a pretty-printed XML string for an Element.

    Todo
    ------

    """
    if isinstance(elem, (Element, ET._Element)):
        rough_string = ET.tostring(elem, encoding=encoding)
    else:
        rough_string = ET.tostring(ET.fromstring(elem), encoding=encoding)
    reparsed = minidom.parseString(rough_string)
    pattern = re.compile(">([.^<>\n]*?)(\s?)<", re.DOTALL)
    return pattern.sub(">\g<2><", reparsed.toprettyxml(indent="  "))
