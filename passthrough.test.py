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
    def setUp(self):
        self.root = os.getcwd()
        self.mp_dir = "mp_test"
        self.base_dir = "base_test"
        self._mp_path = os.path.join(self.root, self.mp_dir)
        self._base_path = os.path.join(self.root, self.base_dir)
        self.md5_file = None
        self.md5dictionary = None


    # Helper Methods
    # ==============
    def makeTestDirs(self):
        if os.path.exists(self._mp_path) or os.path.exists(self._base_path):
            # Delete directory then create a new one
            self.deleteTestDirs()
        os.makedirs(self._mp_path)
        os.makedirs(self._base_path)


    def deleteTestDirs(self):
        if os.path.exists(self._mp_path):
            shutil.rmtree(self._mp_path)
            print("Success: Removed the Mount Path")
        if os.path.exists(self._base_path):
            shutil.rmtree(self._base_path)
            print("Success: Removed the Base Path")


    def createTestFile(self, file, data):
        print("Creating the test file: " + file)
        file_path = os.path.join(self._mp_path, file)
        f = open(file_path, "w")
        f.write(data)
        f.close()


    def generateMD5Hash(self, file_name):
        # Open the file
        file = open(os.path.join(self._base_path, file_name), 'rb')
        # Read contents of the file
        file_data = file.read()
        # Get hash of file
        md5_value = hashlib.md5(file_data).hexdigest()
        return md5_value


    def corruptTestFileHash(file_path):
        print("Corrupting the test file: " + file_path)
        hash = hashlib.md5()


    def deleteTestFile(file_path):
        if os.path.exists(file_path):
            print(file_path)
            os.remove(file_path)
        else:
            print("The file does not exist") 


    def initPassthrough(self):
        self.pt_proc = subprocess.Popen(["python", "passthrough.py", self.base_dir, self.mp_dir])


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
        storedHash = self.md5dictionary["empty.txt"]
        realHash = self.generateMD5Hash("empty.txt")
        print("Hash's Equal: " + str(storedHash == realHash))


    def testDeleteEmptyFile(self):
        # Get path to file = mp_test + file name
        f_path = os.path.join(self.mp_dir, "empty.txt")
        try:
            self.deleteTestFile(f_path)
            print("File [empty.txt] deleted")
        except:
            print("FAILURE: unable to delete file")



    def testDeleteEmptyFileHash(self):
        self.md5_file = os.path.join(self._base_path, ".md5_hashes")
        with open(self.md5_file, "rb") as file:
            self.md5dictionary = pickle.load(file)
        if "empty.txt" in self.md5dictionary:
            print("FAILURE: Hash still found in dictionary.")
        else:
            print("SUCCESS: Hash not found in dictionary.")




# if __name__ == '__main__':
#     unittest.main()


def mainTest():
    test = TestPassthroughMethods()
    test.setUp()
    test.testInitPassthrough()
    time.sleep(1)
    test.testCreateEmptyFile()
    test.testVerifyEmptyFileHash()
    test.testDeleteEmptyFile()
    test.testDeleteEmptyFileHash()
    # test.pt_proc.kill()


mainTest()
