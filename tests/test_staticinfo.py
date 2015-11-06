import unittest
from analyzer.staticInfo_predictor import StaticInfoPredictor

__author__ = 'Jayvee'
'''
Not yet ready
'''

class MyStaticInfoTest(unittest.TestCase):
    # init unittest
    def setUp(self):
        self.predictor = StaticInfoPredictor()

    # exit unittest
    def tearDown(self):
        pass

    def test_staticinfo_predict(self):
        user_applist = []
        # case 1
        result = self.predictor.staticinfo_predict(user_applist, is_local=False, is_degreed=False)
        self.assertEqual(result, {})
        # case 2
        result = self.predictor.staticinfo_predict(user_applist, is_local=True, is_degreed=False)
        self.assertEqual(result, {})
        # case 3
        result = self.predictor.staticinfo_predict(user_applist, is_local=False, is_degreed=True)
        self.assertEqual(result, {})
        # case 4
        result = self.predictor.staticinfo_predict(user_applist, is_local=True, is_degreed=True)
        self.assertEqual(result, {})
