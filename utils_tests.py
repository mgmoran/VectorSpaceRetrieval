""" Unit tests to ensure that the helper functions for the module are functioning properly.

Examples taken from slides"""

import unittest

class TestVectorSpaceModel(unittest.TestCase):

    def setUp(self):
        pass

    def test_letters(self):

    def test_truncation(self):
        self.assertEqual("".join(self.f2.transduce("a33333")[0]), "a333")
        self.assertEqual("".join(self.f2.transduce("123456")[0]), "123")
        self.assertEqual("".join(self.f2.transduce("11")[0]), "11")
        self.assertEqual("".join(self.f2.transduce("5")[0]), "5")

    def test_padding(self):
        self.assertEqual("".join(self.f3.transduce("3")[0]), "300")
        self.assertEqual("".join(self.f3.transduce("b56")[0]), "b560")
        self.assertEqual("".join(self.f3.transduce("c111")[0]), "c111")

    def test_soundex(self):
        self.assertEqual(soundex_convert("jurafsky"), "j612")

    def test_morphology(self):
        havocking = list('havocking')
        self.assertEqual(self.mparser.parse(havocking), "havoc+present participle form")
        lick = ['l','i','c','k','+past form']
        self.assertEqual(self.mparser.generate(lick), "licked")

if __name__ == '__main__':
    unittest.main()
