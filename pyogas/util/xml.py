from xml.etree.ElementTree import tostring
from xml.etree import ElementTree
from xml.dom import minidom


def prettify_xml(elem):
    """
    Return a pretty-printed XML string for an Element.
    """
    rough_string = ElementTree.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
