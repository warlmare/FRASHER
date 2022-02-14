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
import zlib, sys

class NIHTestObjectSimilarity(BaseTest):

    def create_testdata(self, directory_path, target_path):
        '''TODO: explain what it does

        :param filepath:
        :param target_path:
        :return: filepaths: list of filepaths
        '''

        filepaths = []
        needle_paths = []
        files = os.listdir(directory_path)
        for file in files:
            filepaths.append(os.path.join(directory_path,file))

        # create a file where 20% of the head is cutoff
        needle_1_filename = helper.get_file_name(filepaths[0])
        needle_1_filepath = target_path + "/_needle1_" + needle_1_filename
        first_needle = file_manipulation.front_side_cutting(filepaths[0],20)
        f = open(needle_1_filepath, "wb")
        f.write(first_needle)
        f.close()
        needle_paths += [needle_1_filepath]

        # create a file where 20% of the tail is cutoff
        needle_2_filename = helper.get_file_name(filepaths[1])
        needle_2_filepath = target_path + "/_needle2_" + needle_2_filename
        second_needle = file_manipulation.end_side_cutting(filepaths[1], 20)
        f = open(needle_2_filepath, "wb")
        f.write(second_needle)
        f.close()
        needle_paths += [needle_2_filepath]

        # create a file where the first 50% are overwritten with random bytes
        needle_3_filename = helper.get_file_name(filepaths[2])
        needle_3_filepath = target_path + "/_needle3_" + needle_3_filename
        third_needle = file_manipulation.percentage_blocks_random_head_overwrite(filepaths[2],50)
        f = open(needle_3_filepath, "wb")
        f.write(third_needle)
        f.close()
        needle_paths += [needle_3_filepath]

        # create a file where the last 50% are overwritten with random bytes
        needle_4_filename = helper.get_file_name(filepaths[3])
        needle_4_filepath = target_path + "/_needle4_" + needle_4_filename
        fourth_needle = file_manipulation.percentage_blocks_random_tail_overwrite(filepaths[3],50)
        f = open(needle_4_filepath, "wb")
        f.write(fourth_needle)
        f.close()
        needle_paths += [needle_4_filepath]

        # create a file where 200 % of the orig file length in random bytes is prepended to the file
        needle_5_filename = helper.get_file_name(filepaths[4])
        needle_5_filepath = target_path + "/_needle5_" + needle_5_filename
        fifth_needle = file_manipulation.percentage_blocks_random_head_tail_insert(filepaths[4],"percentage_head",200)
        f = open(needle_5_filepath, "wb")
        f.write(fifth_needle)
        f.close()
        needle_paths += [needle_5_filepath]

        # create a file where 200 % of the orig file length in random bytes is appended to the file
        needle_6_filename = helper.get_file_name(filepaths[5])
        needle_6_filepath = target_path + "/_needle6_" + needle_6_filename
        sixth_needle = file_manipulation.percentage_blocks_random_head_tail_insert(filepaths[5], "percentage_tail", 200)
        f = open(needle_6_filepath, "wb")
        f.write(sixth_needle)
        f.close()
        needle_paths += [needle_6_filepath]

        # create two test files that have 50% of their length randomly overwritten with a unrelated file of the same
        # file type
        needle_7_filename = helper.get_file_name(filepaths[6])
        needle_7_filepath = target_path + "/_needle7_" + needle_7_filename
        needle_8_filepath = target_path + "/_needle8_" + needle_7_filename

        filename, file_extension = os.path.splitext(filepaths[6])
        needle_size = helper.getfilesize(filepaths[6])
        chunksize = int(needle_size / 2)

        # we need a file of the same filetype from the testfiles.
        for file in os.listdir("../../testdata/filetype_testfiles"):
            if file.endswith(file_extension):
                chunkfile_path = os.path.join("../../testdata/filetype_testfiles", file)

        seventh_needle, eighth_needle = file_manipulation.common_block_insertion(filepaths[6],
                                                                               filepaths[6],
                                                                               chunkfile_path,
                                                                               chunksize)

        f = open(needle_7_filepath, "wb")
        f.write(seventh_needle)
        f.close()
        needle_paths += [needle_7_filepath]

        f = open(needle_8_filepath, "wb")
        f.write(eighth_needle)
        f.close()
        needle_paths += [needle_8_filepath]


        # create file that has been compressed through zlib
        needle_9_filename = helper.get_file_name(filepaths[7])
        needle_9_filepath = target_path + "/_needle9_" + needle_9_filename
        with open(filepaths[7], mode="rb") as fin, open(needle_9_filepath, mode="wb") as fout:
            data = fin.read()
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            #print(f"Original size: {sys.getsizeof(data)}")
            # Original size: 1000033
            #print(f"Compressed size: {sys.getsizeof(compressed_data)}")
            fout.write(compressed_data)

        needle_paths += [needle_9_filepath]


        # create a file that TODO: Create the 10th needle

        return needle_paths


    def test(self, algorithms:list, testfiles_path:str, filter_directory_path:str) -> list:
        ''' creates a filter with hashes from all the files that
        are contained in the folderpath. It then compares them with a single hash.
        It is evalauted wether the file with the highest similarity score is a
        True positive.

        :param algorithms: the algorithms that should be tested; list with strings.
        :param testfiles_path: path to the files that will be manipulated as needles
        :param filter_directory_path:  path to directory which contains the filter files
        :return: dataframe with results. TODO: syntax ? FP TP TN FN
        '''

        df_list = []
        needle_directory_name = "needle_in_the_haystack_object_similarity"
        needle_directory_path = self.create_testrun_folder(needle_directory_name)
        needle_files_path_list = self.create_testdata(testfiles_path, needle_directory_path)

        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)
            filter = algorithm_instance.get_filter(filter_directory_path)
            filter_len = len(filter)
            testrun_tb = [["needle type", i]]

            for elem in needle_files_path_list:

                needle_filename = helper.get_file_name(elem)

                # we read the type of needle from the filename
                needle_number = re.search(r'\d+', needle_filename).group()

                # this is the original name of the file that was manipulated into a needle
                testfile_name_raw = re.search(r'(\d+)\D+$', needle_filename).group(1)
                print(testfile_name_raw)

                results_dict = algorithm_instance.compare_file_against_filter(filter, elem)

                # The highest matching values are considered true positives
                max_keys = [k for k, v in results_dict.items() if v == max(results_dict.values())]
                print(max_keys)
                filesize = helper.getfilesize(elem)

                if testfile_name_raw in max_keys and not all(value == 0 for value in results_dict.values()):
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
                    FN = 1
                    TN = filter_len - FN - FP


                RATES = "TP: {}, FP: {}, TN: {}, FN: {}".format(TP, FP, TN, FN)

                testrun_tb.append([needle_number,RATES])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=["needle type"
                                                                       ]), df_list)
        return results


if __name__ == '__main__':
    test_instance = NIHTestObjectSimilarity()
    test_files = "../../testdata/pdf"
    filter_dir = "../../../t5"
    algorithms = ["TLSH", "SSDEEP"]
    #needles = test_instance.create_testdata(test_files, target_dir)
    results = test_instance.test(algorithms, test_files , filter_dir)
    print(tabulate(results, headers='keys', tablefmt='psql'))

    #file2 = "../../testdata/20220207-185714_needle_in_the_haystack/random_57"

    #tlsh_instance = algorithms.SSDEEP()
    #filter = tlsh_instance.get_filter(test_dir)
    #print(len(filter))
    #compare_dict = tlsh_instance.compare_file_against_filter(filter, test_file)
    #pprint.pprint(compare_dict)
    #test_instance.create_testdata("../../testdata/testfiles_alignment_robustness", "blib")

