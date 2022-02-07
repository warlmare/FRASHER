import pprint

import lib.hash_functions.algorithms
from base_test import BaseTest
from lib.helpers import helper
from lib.helpers import file_manipulation
from lib.hash_functions import algorithms
import os
from functools import reduce
import pandas as pd
from tabulate import tabulate
import re

class NeedleInTheHaystackTest(BaseTest):

    def create_testdata(self, filepath, target_path):
        '''cuts off random 50% from a file and returns the path to the newly created file

        :param filepath:
        :param target_path:
        :return: filepaths: list of filepaths
        '''

        filepaths = []
        cutoff = 1 # 1
        while cutoff < 100:
            new_file_path = target_path + "/random_" + str(cutoff)
            new_file_byt = file_manipulation.random_cutting_perc(filepath, cutoff)

            f = open(new_file_path, "wb")
            f.write(new_file_byt)
            f.close()

            filepaths += [new_file_path]
            cutoff += 1

        return filepaths


    def test(self, algorithms:list, filepath:str, directory_path:str) -> list:
        ''' creates a filter with hashes from all the files that
        are contained in the folderpath. It then compares them with a single hash.
        It is evalauted wether the file with the highest similarity score is a
        True positive.

        :param algorithms: the algorithms that should be tested; list with strings.
        :param filepath: path to the file that should be searched for among the others in folderpath
        :param directory_path:  path to directory which contains the filter files
        :return: dataframe with results. TODO: syntax ? FP TP TN FN
        '''

        df_list = []
        filename = helper.get_file_name(filepath)
        testfoldername = "needle_in_the_haystack"
        testfolderpath = self.create_testrun_folder(testfoldername)
        file_list = self.create_testdata(filepath, testfolderpath)

        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)
            filter = algorithm_instance.get_filter(directory_path)
            filter_len = len(filter)
            testrun_tb = [["needle size (byte)","cutoff (%)", i]]

            for elem in file_list:

                cutoff_prc = int(re.sub('.*?([0-9]*)$', r'\1', elem))
                results_dict = algorithm_instance.compare_file_against_filter(filter, elem)

                # The highest matching values are considered true positives
                max_keys = [k for k, v in results_dict.items() if v == max(results_dict.values())]
                filesize = helper.getfilesize(elem)


                if filename in max_keys and not all(value == 0 for value in results_dict.values()):
                    TP = 1
                    FP = len(max_keys) - 1
                    TN = filter_len - TP - FP
                    FN = 0
                    # covers the case that all files match with 0
                elif all(value == 0 for value in results_dict.values()) == True:
                    TP = "-"
                    FP = "-"
                    TN = "-"
                    FN = "-"
                else:
                    TP = 0
                    FP = len(max_keys)
                    TN = filter_len - FN - FP
                    FN = 1

                RATES = "TP: {}, FP: {}, TN: {}, FN: {}".format(TP, FP, TN, FN)

                testrun_tb.append([filesize,cutoff_prc,RATES])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=["needle size (byte)",
                                                                       "cutoff (%)"]), df_list)
        return results


if __name__ == '__main__':
    test_instance = NeedleInTheHaystackTest()
    test_file = "../../../t5/test_file5_short"
    test_dir = "../../../t5"
    algorithms = ["TLSH", "SSDEEP"]
    results = test_instance.test(algorithms, test_file , test_dir)
    print(tabulate(results, headers='keys', tablefmt='psql'))

    file2 = "../../testdata/20220207-185714_needle_in_the_haystack/random_57"

    #tlsh_instance = algorithms.SSDEEP()
    #filter = tlsh_instance.get_filter(test_dir)
    #print(len(filter))
    #compare_dict = tlsh_instance.compare_file_against_filter(filter, test_file)
    #pprint.pprint(compare_dict)


