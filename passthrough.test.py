from __future__ import with_statement
from unittest.mock import MagicMock

import passthrough

import unittest
import os
import shutil

class TestPassthroughMethods(unittest.TestCase):
    def __init__(self):
        print("Testing class initalized")
        # END MODIFICATION

    # Helper Methods
    # ==============
    def makeTestDirs(self):
        root = os.getcwd()
        mt_dir = "mt_test"
        base_dir = "base_test"
        mt_test_path = os.path.join(root, mt_dir)
        base_test_path = os.path.join(root, base_dir)
        self._mt_path = mt_test_path
        self._base_path = base_test_path
        
        if os.path.exists(mt_test_path) or os.path.exists(base_test_path):
            # Delete directory then create a new one
            self.deleteTestDirs()

        os.makedirs(mt_test_path)
        os.makedirs(base_test_path)



    def deleteTestDirs(self):
        if os.path.exists(self._mt_path):
            shutil.rmtree(self._mt_path)
            print("Successfully removed the Mount Path")
        if os.path.exists(self._base_path):
            shutil.rmtree(self._base_path)
            print("Successfully removed the Base Path")


    def createTestFile(file):
        print("Creating the test file: " + file)
        f = open(file, "w")
        f.write("somestring")
        f.close()


    def corruptTestFile(file_path):
        print("Corrupting the test file: " + file_path)


    def deleteTestFile(file_path):
        print("Deleting the test file: " + file_path)



    def initPasstrhough(mt_point, rt_point):
        passthrough.main(mountpoint=mt_point, root=rt_point)


    # Unit Tests
    # ==========
    def testInitPasstrough(self):
        print("Testing initialization of program.")
        mt, root = TestPassthroughMethods.makeTestDirs(self)
        print("Success: Directory Creation")
        
        try:
            TestPassthroughMethods.initPasstrhough(mt, root)
            print("Success: Initialization of Passthrough")
        except:
            print("Error: Initialization of Passthrough")



# if __name__ == '__main__':
#     unittest.main()


def mainTest():
    test = TestPassthroughMethods()
    test.testInitPasstrough()


mainTest()
