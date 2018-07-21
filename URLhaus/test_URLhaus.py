import unittest
from URLhaus import URLhaus


class URLhausTest(unittest.TestCase):
    def test_1(self):
        indicator = "hoge.com"
        results = URLhaus(indicator).search()
        self.assertEqual(len(results), 0)

    def test_2(self):
        indicator = "http://eepaulgroupt.club/"
        results = URLhaus(indicator).search()
        self.assertGreater(len(results), 0)

if __name__ == "__main__":
    unittest.main()
