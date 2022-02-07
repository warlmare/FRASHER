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
                max_keys = [k for k, v in results_dict.items() if v == max(results_dict.values())]
                filesize = helper.getfilesize(elem)

                # TODO: catch max_keys.is_empty()
                if filename in max_keys:
                    TP = 1
                    FP = len(max_keys) - 1
                    TN = filter_len - TP - FP
                    FN = 0
                else:
                    TP = 0
                    FP = len(max_keys)
                    TN = filter_len - FN - FP
                    FN = 1

                RATES = "TP: {}, FP: {}, TN: {}, FN: {}".format(TP, FP, TN, FN)

                testrun_tb.append([filesize,cutoff_prc,RATES])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=["testfile",
                                                                       "cutoff (%)"]), df_list)
        return results


if __name__ == '__main__':
    test_instance = NeedleInTheHaystackTest()
    test_file = "../../../t5/002824.gif"
    test_dir = "../../../t5"
    #algorithms = ["SSDEEP"]
    #results = test_instance.test(algorithms, test_file , test_dir)
    #print(tabulate(results, headers='keys', tablefmt='psql'))

    file2 = "../../20220207-154212_needle_in_the_haystack/random_58"

    ssdeep_instance = lib.hash_functions.algorithms.SSDEEP()
    #filter = ssdeep_instance.get_filter(test_dir)
    #compare_dict = ssdeep_instance.compare_file_against_filter(filter, file2)
    #print(compare_dict)
    print(ssdeep_instance.get_hash(file2))

