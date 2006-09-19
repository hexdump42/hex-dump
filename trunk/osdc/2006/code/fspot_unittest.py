import unittest
import clr
clr.AddReference("libgphoto2-sharp.dll")
import LibGPhoto2

class TestLibGPhoto2(unittest.TestCase):
    """
    A simple test case for the FSpot LibGPhoto2 wrapper
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Camera(self):
        self.assert_(LibGPhoto2.Camera(),"Creation of Camera object failed.")

    def test_Context(self):
        self.assert_(LibGPhoto2.Context(),"Creation of Context object failed.")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLibGPhoto2))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
