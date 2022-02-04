from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
from random import randint
from shutil import copy
from pathlib import Path
from typing import Union



class RandomNoiseResistanceTest(BaseTest):

    def create_testdata(self, filepath:str, target_path:str, blocklength:int) -> str:
        '''either deletes inserts or substitutes with equal probability a certain amount of bytes in a file
        ten changes are performed at a time.

        :param filepath: path to the file that serves as an input
        :param target_path: the new file will be saved here
        :param blocklength: the amount of bytes that will be changed


        :return: filepath to the newly created file,
                 deleted_bytes, substituted_bytes, inserted_bytes
        '''

        if Path(target_path).is_file():
            # if the file already exists from previous calls
            new_file_path = target_path
        else:
            # if the file is created for the first time
            new_file_path = target_path + "/" + str(blocklength)
            # the file that will be manipulated is created
            copy(filepath, new_file_path)

        # syntax [[del, deletion_start_offset, deletion_end_offset],
        # ... , [sub, substitution_start_offset, substitution_end_offset],
        # ... , [ins, insertion_start_offset, insertion_end_offset]]
        change_log = []

        # ten manipulations are done at once so (blocklength / 10) is the length of bytes changed  in a single moment
        single_manipulation_length = int(blocklength / 10)

        for _ in range(10):
            rand_ch = randint(1,3)

            # random deletion
            if rand_ch == 1:
                new_file_byt, offset = file_manipulation.random_cutting_byte(new_file_path, single_manipulation_length)
                change_log.append(["del", offset, offset + single_manipulation_length])
            # random substitution
            elif rand_ch == 2:
                new_file_byt, offset = file_manipulation.random_substitution(new_file_path, single_manipulation_length)
                change_log.append(["sub", offset, offset +  single_manipulation_length])

            # random insertion
            else:
                new_file_byt, offset = file_manipulation.random_insertion(new_file_path, single_manipulation_length)
                change_log.append(["ins", offset, offset + single_manipulation_length])


            f = open(new_file_path, "wb")
            f.write(new_file_byt)
            f.close()


        return new_file_path, change_log


    # TODO: change factor omits how much of the original file is still there we need tracking for that.
    # TODO: it is unclear from the FRASH1.0 Documentation wether single bytes are changed or multiple bytes at a time
    def test(self, algorithm:str, filepath:str):
        '''random noise resistance test

        :param algorithm: algorithm used for approximate matching
        :param filepath: file that will be cutoff
        :return: testrun_tb:  list of arrays with results, first element is headers, filesize, cutoff %, similarity score
        '''

        testfoldername = "random_noise_resistance_" + algorithm
        testfolderpath = self.create_testrun_folder(testfoldername)

        # counts how many changes the file has undergone
        change_ctr = 10
        testrun_tb = [["changes","similarity score", "change factor"]]
        filesize = helper.getfilesize(filepath)
        log = [filesize,[],[]]
        
        testfile, changelog = self.create_testdata(filepath, testfolderpath, 5000)
        curr_log = self.manipulation_log_update(changelog, log)
        
        
        if algorithm == "tlsh":
            testrun_tb = [["changes", "tlsh distance score", "change factor"]]
            instance = algorithms.TLSH()
            score = instance.compare_file_against_file(filepath, testfile)

            resistance_score = ((change_ctr * 500) / filesize) * 100
            testrun_tb.append([change_ctr, score, resistance_score])

            while score < 300:

                change_ctr += 10
                testfile, changelog = self.create_testdata(testfile, testfile, 5000)
                curr_log = self.manipulation_log_update(changelog, curr_log)
                file_state = self.get_log_arr(curr_log)
                print(self.get_log_scale(file_state))

                score = instance.compare_file_against_file(filepath, testfile)
                resistance_score = ((change_ctr * 500) / filesize) * 100
                testrun_tb.append([change_ctr, score, resistance_score])

            else:
                print("file can no longer be matched")

            file_state = self.get_log_arr(curr_log)
            print(self.get_log_scale(file_state))
            return testrun_tb
        else:
            print("Algorithm not yet supported")

if __name__ == '__main__':
    
    testinstance = RandomNoiseResistanceTest()
    testfile1 = "../../testdata/test_file3"
    #folder = testinstance.create_testrun_folder("foo")
    
    #testinstance.create_testdata(testfile1,folder,50)
    result = testinstance.test("tlsh",testfile1)
    print(tabulate(result))

                






