import io

import lxml.etree
import lxml.html

from cssselect import GenericTranslator

LATIN_1_NBSP = '\xa0'


def css_to_xpath(css_selector: str) -> GenericTranslator:
    return GenericTranslator().css_to_xpath(css_selector)


def get_cleaned_text(el: lxml.etree.Element) -> str:
    """
    >>> get_cleaned_text(lxml.html.fromstring(r'<span>Some text inside.</span>'))
    'Some text inside.'
    >>> get_cleaned_text(lxml.html.fromstring(r'<div>Some <span>nested</span> text.</div>'))
    'Some nested text.'
    >>> get_cleaned_text(lxml.html.fromstring(r'<div>    Text with whitespace.\t\t</div>'))
    'Text with whitespace.'
    >>> get_cleaned_text(lxml.html.fromstring(r'<div>Text&nbsp;with&nbsp;non-breakable&nbsp;spaces.</div>'))
    'Text with non-breakable spaces.'
    """
    text = lxml.etree.XPath("string()")(el)
    text = text.replace(LATIN_1_NBSP, " ")
    text = text.strip()

    return text


def parse_html(html: str) -> lxml.etree.Element:
    parser = lxml.etree.HTMLParser()
    tree = lxml.etree.parse(io.StringIO(html), parser)

    return tree
