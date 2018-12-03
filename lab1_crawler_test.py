__author__ = 'ceciliawu'

import unittest
from crawler import crawler

class CrawlerTester(unittest.TestCase):
    _crawler = None
    def test_get_inverted_index(self):
        self._crawler = crawler(None,'urls.txt')
        expected_inverted_index = {
            1:set([1,2]),
            2:set([1]),
            3:set([1]),
            4:set([2]),
            5:set([2])
        }

        self._crawler.crawl(1)
        returned_result = self._crawler.get_inverted_index()
        self.assertEqual(expected_inverted_index, returned_result)


    def test_get_resolved_inverted_index(self):
        self._crawler = crawler(None,'urls.txt')
        expected_resolved_inverted_index={
            u'csc326':set(['http://www.eecg.toronto.edu/~jzhu/csc326/csc326proj.html','http://www.eecg.toronto.edu/~jzhu/csc326/csc326.html']),
            u'machine':set(['http://www.eecg.toronto.edu/~jzhu/csc326/csc326proj.html']),
            u'project':set(['http://www.eecg.toronto.edu/~jzhu/csc326/csc326proj.html']),
            u'programming':set(['http://www.eecg.toronto.edu/~jzhu/csc326/csc326.html']),
            u'languages':set(['http://www.eecg.toronto.edu/~jzhu/csc326/csc326.html'])
        }
        self._crawler.crawl(1)
        returned_result = self._crawler.get_resolved_inverted_index()
        self.assertEqual(expected_resolved_inverted_index,returned_result)

if __name__ == '__main__':
    unittest.main()
