from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
import re
from functools import reduce
import pandas as pd

class AlignmentRobustnessTest(BaseTest):

    def create_testdata(self, filepath, target_path, max_blocklength, stepsize, mode) -> list:
        '''Creates a set of testfiles that have a certain amount of random bytes inserted at the beginning
        either a fixed percentage or block size, the amount of inserted bytes is increasing.

        :param filepath: the path of the file
        :param target_path: the new file will be saved to this location
        :param mode: either fixed of percentage
        :param blocklength: size either in percentages or in KB blocks

        :return: list of filepaths with newly created files
        '''

        filepaths = []
        current_blocklength = 0

        while current_blocklength < max_blocklength:
            current_blocklength += stepsize
            filesize = helper.getfilesize(filepath)
            new_file_path = target_path + "/" + mode + "_" + str(current_blocklength)

            if mode == "fixed":
                new_file_byt = file_manipulation.fixed_blocks_random_head(filepath, current_blocklength)
            elif mode == "percentage":
                new_file_byt = file_manipulation.percentage_blocks_random_head(filepath, current_blocklength)

            f = open(new_file_path, "wb")
            f.write(new_file_byt)
            f.close()

            filepaths += [new_file_path]

        return filepaths


    def test(self, algorithms:list, filepath:str, max_blocklength, stepsize:int, mode:str) -> list:
        '''alignment robustness test for a specified algorithm.

        Analyzes the impact on approximate matching when inserting byte sequences at the beginning of
        an input either of fixed size size or percentage blocks.

        :param algorithms: list of algorithms used for approximate matching
        :param mode: either "fixed" KB will be inserted or "percentage" blocks
        :param filepath: path of the file that will be manipulated
        :param max_blocklength: is the maximum block size that will be inserted into the file in bytes
        :param stepsize: the inserted blocks will increase by a specified amount either in percent or bytes
        :return dataframe with the results. Syntax: filesize, blocksize, blocksize %, similarity score

        '''

        testfoldername = "alignment_robustness"
        testfolderpath = self.create_testrun_folder(testfoldername)
        file_list = self.create_testdata(filepath, testfolderpath, max_blocklength, stepsize, mode)
        df_list = []

        #TODO: mode: "percentage" needs a whole other calculation this needs to be addressed with if mode = ...
        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)
            testrun_tb = [["filesize (bytes)", "blocksize (bytes)", "blocksize (%)", i]]

            for elem in file_list:
                filesize = helper.getfilesize(filepath)
                score = algorithm_instance.compare_file_against_file(algorithm_instance, filepath, elem)
                current_blocklength = int(re.sub('.*?([0-9]*)$',r'\1',elem))
                blocksize_perc = round((current_blocklength / filesize) * 100, 2)
                testrun_tb.append([filesize, current_blocklength, blocksize_perc, score])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=['filesize (bytes)',
                                                                       "blocksize (bytes)",
                                                                       "blocksize (%)"]), df_list)

        return results

if __name__ == '__main__':
    testinstance = AlignmentRobustnessTest()
    testfile = "../../testdata/test_file3"

    algorithms = ["SSDEEP", "TLSH", "MRSHCF"]
    results = testinstance.test(algorithms, testfile, 1000000, 50000, "fixed")
    #results = testinstance.test(algorithms, testfile, 100, 5, "percentage")
    print(tabulate(results, headers='keys', tablefmt='psql'))
