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
            print("SUCCESS: Removed the Mount Path")
        if os.path.exists(self._base_path):
            shutil.rmtree(self._base_path)
            print("SUCCESS: Removed the Base Path")


    def createTestFile(self, file, data):
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


    def corruptTestFileHash(self, file_name):
        corrupted_data = "This is corrupted data"
        # Generate fake hash
        md5_value = hashlib.md5(corrupted_data.encode('utf-8')).hexdigest()
        self.md5dictionary[file_name] = md5_value
        self.saveHashes()


    def deleteTestFile(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist") 


    def initPassthrough(self):
        self.pt_proc = subprocess.Popen(["python", "passthrough.py", self.base_dir, self.mp_dir])


    def getMD5Values(self):
        self.md5_file = os.path.join(self._base_path, ".md5_hashes")
        with open(self.md5_file, "rb") as file:
            self.md5dictionary = pickle.load(file)


    def saveHashes(self):
        with open(self.md5_file, "wb") as file:
            pickle.dump(self.md5dictionary, file)


    #    Tests    #
    # =========== #
    def testInitPassthrough(self):
        TestPassthroughMethods.makeTestDirs(self)
        print("SUCCESS: Directory Creation")
        
        try:
            TestPassthroughMethods.initPassthrough(self)
            print("SUCCESS: Initialization of Passthrough")
        except:
            print("FAILURE: Initialization of Passthrough")

    
    def testCreateEmptyFile(self):
        f_name = "empty.txt"
        f_data = ""
        try:
            self.createTestFile(f_name, f_data)
        except:
            print("FAILURE: Could not create the file " + f_name)


    def testVerifyEmptyFileHash(self):
        self.getMD5Values()
        storedHash = self.md5dictionary["empty.txt"]
        realHash = self.generateMD5Hash("empty.txt")
        if storedHash == realHash:
            print("SUCCESS: Checksum verification")
        else:
            print("FAILUE: Checksum verification")


    def testDeleteEmptyFile(self):
        # Get path to file = mp_test + file name
        f_path = os.path.join(self.mp_dir, "empty.txt")
        try:
            self.deleteTestFile(f_path)
            print("SUCCESS: File [empty.txt] deleted")
        except:
            print("FAILURE: unable to delete file")



    def testDeleteEmptyFileHash(self):
        self.getMD5Values()
        if "empty.txt" in self.md5dictionary:
            print("FAILURE: Hash still found in dictionary.")
        else:
            print("SUCCESS: Hash not found in dictionary.")


    def testCorruptFileHash(self):
        print("Checking to see if correct warning pops up")
        self.corruptTestFileHash("empty.txt")
        self.getMD5Values()
        storedHash = self.md5dictionary["empty.txt"]
        realHash = self.generateMD5Hash("empty.txt")
        if realHash != storedHash:
            print("SUCCESS: Hash Corrupted.")
            print("\tReal Checksum: " + str(realHash))
            print("\tStored Hash: " + str(storedHash))


    def shutdownPassthrough(self):
        # Run `fusermount -u mp_test/`
        os.popen('fusermount -u mp_test/')


# if __name__ == '__main__':
#     unittest.main()


def mainTest():
    test = TestPassthroughMethods()
    test.setUp()
    test.testInitPassthrough()
    time.sleep(1)
    test.shutdownPassthrough()
    # test.testCreateEmptyFile()
    # test.testVerifyEmptyFileHash()
    # test.testCorruptFileHash()
    # Comment these out for now. Don't want them to run just yet
    # test.testDeleteEmptyFile()
    # test.testDeleteEmptyFileHash()
    # test.pt_proc.kill()


mainTest()
