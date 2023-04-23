from __future__ import with_statement

import subprocess
import passthrough
import pickle
import unittest
import os
import shutil
import hashlib
import time


class PassthroughTest():
    def __init__(self):
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
        if os.path.exists(self._base_path):
            shutil.rmtree(self._base_path)


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


    def corruptTestFile(self, file_name):
        corrupted_data = "This is corrupted data. This will mess up our verification"
        # Save file
        file_path = os.path.join(self._base_path, file_name)
        f = open(file_path, "w")
        f.write(corrupted_data)
        f.close()

    def deleteTestFile(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("\tERROR: The named file does not exist") 


    def initPassthrough(self):
        self.pt_proc = subprocess.Popen(["python", "passthrough.py", self.base_dir, self.mp_dir])


    def getMD5Values(self):
        self.md5_file = os.path.join(self._base_path, ".md5_hashes")
        with open(self.md5_file, "rb") as file:
            self.md5dictionary = pickle.load(file)


    def accessCorruptedFile(self, file_name):
        command = 'cat ' + os.path.join(self.mp_dir, file_name)
        os.popen(command)


    def saveHashes(self):
        with open(self.md5_file, "wb") as file:
            pickle.dump(self.md5dictionary, file)


    def shutdownPassthrough(self):
        # Run `fusermount -u mp_test/`
        os.popen('fusermount -u mp_test/')


    #    Tests    #
    # =========== #
    def testInitPassthrough(self):
        print("=== TESTING SET UP OF PASSTHROUGH ===")
        self.makeTestDirs()
        print("\tSUCCESS: Directory Creation")
        
        try:
            self.initPassthrough()
            print("\tSUCCESS: Initialization of Passthrough")
        except:
            print("\tFAILURE: Initialization of Passthrough")

    
    def testCreateEmptyFile(self):
        f_name = "empty.txt"
        f_data = ""
        try:
            self.createTestFile(f_name, f_data)
        except:
            print("\tFAILURE: Could not create the file " + f_name)


    def testVerifyEmptyFileHash(self):
        print("=== TESTING CHECKSUM VERIFICATION ===")
        self.getMD5Values()
        storedHash = self.md5dictionary["empty.txt"]
        realHash = self.generateMD5Hash("empty.txt")
        if storedHash == realHash:
            print("\tSUCCESS: Checksum verification")
        else:
            print("\tFAILUE: Checksum verification")


    def testDeleteEmptyFile(self):
        print("=== TESTING FILE DELETION ===")
        # Get path to file = mp_test + file name
        f_path = os.path.join(self.mp_dir, "empty.txt")
        try:
            self.deleteTestFile(f_path)
            print("\tSUCCESS: File [empty.txt] deleted")
        except:
            print("\tFAILURE: unable to delete file")


    def testDeleteEmptyFileHash(self):
        print("=== TESTING CHECKSUM DELETION ===")
        self.getMD5Values()
        if "empty.txt" in self.md5dictionary:
            print("\tFAILURE: Hash still found in dictionary.")
        else:
            print("\tSUCCESS: Hash not found in dictionary.")


    def testCorruptFile(self):
        print("=== TESTING FILE CORRUPTION DETECTION ===")
        self.corruptTestFile("empty.txt")
        self.initPassthrough()
        # Wait for process to start back up again
        time.sleep(1)
        self.accessCorruptedFile("empty.txt")


def mainTest():
    test = PassthroughTest()
    test.testInitPassthrough()
    time.sleep(1)
    test.testCreateEmptyFile()
    test.testVerifyEmptyFileHash()
    test.shutdownPassthrough()
    test.testCorruptFile()
    time.sleep(1)
    # Comment these out for now. Don't want them to run just yet
    test.testDeleteEmptyFile()
    test.testDeleteEmptyFileHash()
    test.shutdownPassthrough()


mainTest()
