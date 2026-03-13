import unittest

from src.main import detect


class TestDetect(unittest.TestCase):
    def test_callable(self):
        """
        Test that it can be called from other app
        """
        data = [2, 700, 770, 40, 46, 99, 20, 30, 43, 45, 80]
        result = detect("dataset/01.png")
        self.assertEqual(result, data)


if __name__ == "__main_":
    unittest.main()
