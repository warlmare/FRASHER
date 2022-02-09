from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
import pandas as pd
import re
from functools import reduce
from random import randint
class FragmentDetectionTest(BaseTest):


    def create_testdata_debug(self, filepath, target_path, cutoff_init, mode) -> str:
        '''creates single manipulated file that will be used in the test
        a fragment of a file is created through cutting of bits at the end or at random (mode)

        :param filepath1: path to the fil
        :param target_path: the new file will be saved here
        :param cutoff: every turn this amount is cut off from the file

        :return: filepath to newly created file
        '''

        filepaths = []
        cutoff = cutoff_init

        while cutoff < 100:

            new_file_path = target_path + "/" + mode + "_" + str(cutoff)
            if mode == "random":
                rand_ch = randint(0, 1)
                if rand_ch == 0:
                    new_file_byt = file_manipulation.front_side_cutting(filepath, cutoff)
                if rand_ch == 1:
                    new_file_byt = file_manipulation.end_side_cutting(filepath, cutoff)
            elif mode == "end_side_cutting":
                new_file_byt = file_manipulation.end_side_cutting(filepath, cutoff)

            f = open(new_file_path, "wb")
            f.write(new_file_byt)
            f.close()

            filepaths += [new_file_path]
            if cutoff >= 95:
                #according to Breitingers FRASH a cutoff above 95% should be increased 1% at a time. ...
                cutoff += 1
            else:
                cutoff += cutoff_init

        return filepaths

    def test_debug(self, algorithms:list, mode:str, filepath:str) -> list:
        '''fragment-detection test

        :param algorithm: algorithm used for approximate matching
        :param mode: cutoff mode (random or end-side-cutting)
        :param filepath: file that will be cutoff
        :param cutoff_prc: states how much of the file ought to be cut-off step by step
        :return testrun_tb:  dataframe with the results. Syntax of the table is filesize, cutoff %, similarity score
        '''

        testfoldername = "fragment_detection"
        testfolderpath = self.create_testrun_folder(testfoldername)
        filesize = helper.getfilesize(filepath)
        cutoff = 5 # the default cut-off is set to 5 percent
        file_list = self.create_testdata_debug(filepath, testfolderpath, cutoff, mode)
        df_list = []

        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)
            testrun_tb = [["filesize (bytes)", "cutoff size %",i]]

            for elem in file_list:

                scores = []

                for x in range(5):
                    scores += [algorithm_instance.compare_file_against_file(
                                                                            filepath,
                                                                            elem)]
                score = sum(scores) / len(scores)
                cutoff_prc = int(re.sub('.*?([0-9]*)$',r'\1',elem))
                filesize_new = helper.getfilesize(elem)
                testrun_tb.append([filesize_new, cutoff_prc, score])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=["filesize (bytes)",
                                                                       "cutoff size %"]), df_list)

        return results






if __name__ == '__main__':
    testinstance = FragmentDetectionTest()

    testfile = "../../../t5/001673.pdf"

    #testrun = testinstance.test("tlsh", "random", testfile,5)
    #print(tabulate(testrun)) # TODO: this needs to be outsourced into a log module

    algorithms = ["SSDEEP", "TLSH", "MRSHCF"]
    results = testinstance.test_debug(algorithms, "random", testfile)
    print(tabulate(results, headers='keys', tablefmt='psql'))






