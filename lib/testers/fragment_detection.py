from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
import pandas as pd
import re
from functools import reduce

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
                new_file_byt = file_manipulation.random_cutting_perc(filepath, cutoff)
            elif mode == "end_side_cutting":
                new_file_byt = file_manipulation.end_side_cutting(filepath, cutoff)

            f = open(new_file_path, "wb")
            f.write(new_file_byt)
            f.close()

            filepaths += [new_file_path]
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
        cutoff = 1 # the default cut-off is set to 1 percent
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

    def create_testdata(self, filepath, target_path, cutoff, mode) -> str:
        '''creates single manipulated file that will be used in the test
        a fragment of a file is created through cutting of bits at the end or at random (mode)

        :param filepath1: path to the fil
        :param target_path: the new file will be saved here
        :param cutoff: that is made from the file in %

        :return: filepath to newly created file
        '''

        # create new instance of test to create testfile folder
        # testinstance2 = BaseTest() TODO: deprecated

        new_file_path =  target_path + "/" +  mode + "_" + str(cutoff)

        # bytes of the newly created file
        if mode == "random":
            new_file_byt = file_manipulation.random_cutting_perc(filepath, cutoff)
        elif mode == "end_side_cutting":
            new_file_byt = file_manipulation.end_side_cutting(filepath, cutoff)

        f = open(new_file_path, "wb")
        f.write(new_file_byt)
        f.close()

        return new_file_path

    def test(self, algorithm, mode, filepath, cutoff_prc) -> list:
        '''fragment-detection test

        :param algorithm: algorithm used for approximate matching
        :param mode: cutoff mode (random or end-side-cutting)
        :param filepath: file that will be cutoff
        :param cutoff_prc: states how much of the file ought to be cut-off step by step
        :return testrun_tb:  list of arrays with results, first element is headers, filesize, cutoff %, similarity score
        '''

        testfoldername = "fragment_detection_" + algorithm
        testfolderpath = self.create_testrun_folder(testfoldername)
        filesize = helper.getfilesize(filepath)

        #The initial cutoff value is saved here
        cutoff_prc_init = cutoff_prc

        # array where all the results of the testrun are saved TODO: pull into superclass
        testrun_tb = [["filesize (bytes)", "cutoff size (bytes)", "cutoff size %", "similarity score"]]

        first_testfile = self.create_testdata(filepath, testfolderpath, cutoff_prc, mode)


        if algorithm == "tlsh":
            testrun_tb = [["filesize (bytes)", "cutoff size %", "tlsh distance score"]]
            instance = algorithms.TLSH()
            score = instance.compare_file_against_file(filepath, first_testfile)

            filesize_new = filesize - (filesize - helper.getfilesize(first_testfile)) #TODO: way to complicated
            testrun_tb.append([filesize_new, cutoff_prc, score])

            while score < 300:

                #the cutoff is increased by the same amount
                cutoff_prc += cutoff_prc_init
                fragment = self.create_testdata(filepath, testfolderpath, cutoff_prc, mode)
                score = instance.compare_file_against_file(filepath,fragment)

                #this calculates the size of the new file - cutoff
                filesize_new = filesize - (filesize - helper.getfilesize(fragment)) #TODO: way to complicated

                testrun_tb.append([filesize_new, cutoff_prc, score])

            else:
                print("files can no longer be matched by the algorithm")

            return testrun_tb

        else:
            print("algorithm not yet implmeneted")






if __name__ == '__main__':
    testinstance = FragmentDetectionTest()

    testfile = "../../testdata/test_file3"

    #testrun = testinstance.test("tlsh", "random", testfile,5)
    #print(tabulate(testrun)) # TODO: this needs to be outsourced into a log module

    algorithms = ["SSDEEP", "TLSH", "MRSHCF"]
    results = testinstance.test_debug(algorithms, "random", testfile)
    print(tabulate(results, headers='keys', tablefmt='psql'))






