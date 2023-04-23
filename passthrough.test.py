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
    def makeTestDirs():
        root = os.getcwd()
        mt_dir = "mt_test"
        base_dir = "base_test"
        mt_test_path = os.path.join(root, mt_dir)
        base_test_path = os.path.join(root, base_dir)
        os.makedirs(mt_test_path)
        os.makedirs(base_test_path)
        return mt_test_path, base_test_path


    def deleteTestDirs(mt_path, base_path):
        if os.path.exists(mt_path):
            shutil.rmtree(mt_path)
            print("Successfully removed the Mount Path")
        if os.path.exists(base_path):
            shutil.rmtree(base_path)
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
    def testInitPasstrough():
        print("Testing initialization of program.")
        mt, root = TestPassthroughMethods.makeTestDirs()
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


mainTest()