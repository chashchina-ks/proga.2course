import unittest
from main import two_sum

class TestTwoSum(unittest.TestCase):

    def test_example1(self):
        nums = [2, 7, 11, 15]
        target = 9
        expected = [0, 1]
        actual = two_sum(nums, target)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_example2(self):
        nums = [3, 2, 4]
        target = 6
        expected = [1, 2]
        actual = two_sum(nums, target)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_example3(self):
        nums = [3, 3]
        target = 6
        expected = [0, 1]
        actual = two_sum(nums, target)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_no_solution(self):
        nums = [1, 2, 3]
        target = 10
        actual = two_sum(nums, target)
        self.assertIsNone(actual)

    def test_negative(self):
        nums = [-13, -3, 7, 2]
        target = -6
        expected = [0, 2]
        actual = two_sum(nums, target)
        self.assertEqual(sorted(actual), sorted(expected))

if __name__ == '__main__':
    unittest.main()
