from __future__ import with_statement

import subprocess
import passthrough
import pickle
import unittest
import os
import shutil
import hashlib
import time


class TestPassthroughMethods(unittest.TestCase):
    def __init__(self):
        print("Testing class initalized")
        # END MODIFICATION

    # Helper Methods
    # ==============
    def makeTestDirs(self):
        root = os.getcwd()
        self.mt_dir = "mp_test"
        self.base_dir = "base_test"
        mp_test_path = os.path.join(root, self.mt_dir)
        base_test_path = os.path.join(root, self.base_dir)
        self._mt_path = mp_test_path
        self._base_path = base_test_path

        if os.path.exists(mp_test_path) or os.path.exists(base_test_path):
            # Delete directory then create a new one
            self.deleteTestDirs()

        os.makedirs(mp_test_path)
        os.makedirs(base_test_path)



    def deleteTestDirs(self):
        if os.path.exists(self._mt_path):
            shutil.rmtree(self._mt_path)
            print("Success: Removed the Mount Path")
        if os.path.exists(self._base_path):
            shutil.rmtree(self._base_path)
            print("Success: Removed the Base Path")


    def createTestFile(self, file, data):
        print("Creating the test file: " + file)
        file_path = os.path.join(self._mt_path, file)
        f = open(file_path, "w")
        f.write(data)
        f.close()


    def generateMD5Hash(self, file_name):
        # Open the file
        file = open(file_name, 'rb')
        # Read contents of the file
        file_data = file.read()
        # Get hash of file
        md5_value = hashlib.md5(file_data).hexdigest()
        return md5_value


    def corruptTestFileHash(file_path):
        print("Corrupting the test file: " + file_path)
        hash = hashlib.md5()


    def deleteTestFile(file_path):
        print("Deleting the test file: " + file_path)



    def initPassthrough(self):
        self.pt_proc = subprocess.Popen(["python", "passthrough.py", self.base_dir, self.mt_dir])


    #    Tests    #
    # =========== #
    def testInitPassthrough(self):
        TestPassthroughMethods.makeTestDirs(self)
        print("Success: Directory Creation")
        
        try:
            TestPassthroughMethods.initPassthrough(self)
            print("Success: Initialization of Passthrough")
        except:
            print("Error: Initialization of Passthrough")

    
    def testCreateEmptyFile(self):
        
        print("Testing creation of files & MD5 Hash")
        f_name = "empty.txt"
        f_data = ""
        try:
            self.createTestFile(f_name, f_data)
        except:
            print("FAILURE: Could not create the file " + f_name)


    def testVerifyEmptyFileHash(self):
        self.md5_file = os.path.join(self._base_path, ".md5_hashes")
        with open(self.md5_file, "rb") as file:
            self.md5dictionary = pickle.load(file)
        print(self.md5dictionary["empty.txt"])
        print(self.generateMD5Hash("empty.txt"))
        


# if __name__ == '__main__':
#     unittest.main()


def mainTest():
    test = TestPassthroughMethods()
    test.testInitPassthrough()
    time.sleep(1)
    test.testCreateEmptyFile()
    test.testVerifyEmptyFileHash()
    # test.pt_proc.kill()


mainTest()
