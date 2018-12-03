__author__ = 'ceciliawu'

import unittest
import q1
import q2
import q3
import q5

class AssignmentTester(unittest.TestCase):
    def test_q1(self):
        self.assertEqual(4, q1.gcd(12,16))
        self.assertEqual(1, q1.gcd(12,13))
        self.assertEqual(2,q1.gcd(6,8))

    def test_q2(self):
        self.assertEqual("cdeab",q2.rotate_word("abcde",2))
        self.assertEqual("abc",q2.rotate_word("abc",9))

    def test_q3(self):
        l=[]
        f = q3.fib(6,l)
        self.assertEqual(8,f)
        self.assertEqual([6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4],l)

    def test_q5(self):
        D = [100,150,180]
        self.assertEqual([18,22,24],q5.Q(D))




if __name__ == '__main__':
    unittest.main()
