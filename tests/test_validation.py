"""Fast safety regressions; no native vectorizer or renderer required."""
import unittest
from scripts import vectorize as tool


class ValidationTests(unittest.TestCase):
    def svg(self, body):
        return f'<svg xmlns="{tool.SVG}" width="1" height="1" viewBox="0 0 1 1">{body}</svg>'

    def test_rejects_external_css_and_unknown_attributes(self):
        attributes = [
            'style="fill:URL(https://example.invalid/image)"',
            r'style="fill:u\72l(https://example.invalid/image)"',
            'style="fill:url/**/(https://example.invalid/image)"',
            'fill="URL(https://example.invalid/image)"',
            'fill="url(#alpha)"',  # masks belong to the mask attribute only
            'xml:base="https://example.invalid/"',
            'onclick="alert(1)"',
            'xmlns:x="urn:test" x:onload="alert(1)"',
            'xmlns:x="http://www.w3.org/1999/xlink" x:href="https://example.invalid/"',
        ]
        for attr in attributes:
            with self.subTest(attr=attr), self.assertRaises(tool.VectorizeError):
                tool.validate_svg(self.svg(f'<path d="M0 0L1 1" {attr}/>'), (1, 1))

    def test_accepts_generated_mask_and_color_subset(self):
        body = ('<defs><mask id="alpha" style="mask-type:luminance">'
                '<path d="M0 0L1 1" fill="#fff"/></mask></defs>'
                '<g mask="url(#alpha)"><path d="M0 0L1 1" fill="red"/></g>')
        tool.validate_svg(self.svg(body), (1, 1))

    def test_missing_and_duplicate_ids(self):
        for body in ['<g mask="url(#missing)"/>', '<g id="same"/><g id="same"/>']:
            with self.subTest(body=body), self.assertRaises(tool.VectorizeError):
                tool.validate_svg(self.svg(body), (1, 1))

    def test_dtd_and_entities(self):
        for declaration in ['<!DOCTYPE svg>', '<!ENTITY x "test">', '<?xml-stylesheet href="https://example.invalid/x.css"?>']:
            with self.subTest(declaration=declaration), self.assertRaises(tool.VectorizeError):
                tool.validate_svg(declaration + self.svg(''), (1, 1))


if __name__ == '__main__':
    unittest.main()
