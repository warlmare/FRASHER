from lib.testers.base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate

import pandas as pd
import re
from functools import reduce
from random import randint
import matplotlib.pyplot as plt
import os

import random
import string
import tlsh
import nltk
nltk.download('words')
from nltk.corpus import words
from random import sample
from lorem.text import TextLorem

dirname = os.path.dirname(__file__)

class DigestComparisonImpediment(BaseTest):



    def create_testdata(self, testfile_size, multiplication_factor):


        testfile_paths = []

        # official testfile directory
        directory_path = os.path.join(dirname, "../../testdata/digest_comparison_impediment_testfiles")

        # create random bytes
        #testfile_bytes = file_manipulation.random_byte_generation(testfile_size)
        testfile_bytes = file_manipulation.get_rand_chunk_of_ext("jpg",testfile_size)


        testfile_sizes = [testfile_size * y for y in range(1, multiplication_factor)]

        for elem in testfile_sizes:
            filesize = elem
            multiplication_factor_curr = testfile_sizes.index(elem)  +1

            filepath_testfile = directory_path + "/" + str(elem)
            testfile_bytes_x = testfile_bytes * multiplication_factor_curr
            helper.write_bytes_to_file(filepath_testfile, testfile_bytes_x)
            testfile_paths += [filepath_testfile]


        return testfile_paths



    def test(self, algorithms_list, testfile_size, multiplication_factor):

        testdata_paths_list = self.create_testdata(testfile_size, multiplication_factor)

        df_list = []

        initial_testfile = testdata_paths_list[0]


        for algo in algorithms_list:
            algorithms_instance = helper.get_algorithm(algo)
            testrun_tb = [["filesize", algo]]

            for testfile in testdata_paths_list:

                sim_score = algorithms_instance.compare_file_against_file(testfile,
                                                                          initial_testfile)
                f_size = helper.getfilesize(testfile)
                testrun_tb.append([f_size, sim_score])
                res_df = helper.get_dataframe(testrun_tb)

            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=["filesize"]), df_list)
        return results


if __name__ == '__main__':
    testinstance = DigestComparisonImpediment()
    algorithms = ["SSDEEP", "TLSH", "MRSHCF", "MRSHV2", "SDHASH", "FBHASH"]
    results = testinstance.test(algorithms, 5000, 40)

    print(tabulate(results, headers='keys', tablefmt='psql'))
    results.to_csv(os.path.join(dirname, '../../results/digest_comparison_impediment_JPG.csv'))

