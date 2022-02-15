from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
import re
from functools import reduce
import pandas as pd
import os
import matplotlib.pyplot as plt

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
                new_file_byt = file_manipulation.fixed_blocks_random_head_insert(filepath, current_blocklength)
            elif mode == "percentage_head" or "percentage_tail":
                new_file_byt = file_manipulation.percentage_blocks_random_head_tail_insert(filepath,
                                                                                           mode,
                                                                                           current_blocklength)

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
            if mode == "fixed":
                testrun_tb = [["filesize (bytes)", "blocksize (bytes)", "blocksize (%)", i]]
            elif mode == "percentage_head" or "percentage_tail":
                testrun_tb = [["filesize (bytes)", "blocksize (%)", i]]

            for elem in file_list:
                filesize = helper.getfilesize(elem)
                score = algorithm_instance.compare_file_against_file(elem, filepath)

                current_blocklength = int(re.sub('.*?([0-9]*)$',r'\1',elem))
                if mode == "fixed":
                    blocksize_perc = round((current_blocklength / filesize) * 100, 2)
                    testrun_tb.append([filesize, current_blocklength, blocksize_perc, score])
                elif mode == "percentage_head" or "percentage_tail":
                    testrun_tb.append([filesize, current_blocklength, score])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        if mode == "fixed":
            results = reduce(lambda left, right: pd.merge(left, right, on=['filesize (bytes)',
                                                                           "blocksize (bytes)",
                                                                           "blocksize (%)"]), df_list)
        elif mode == "percentage_head" or "percentage_tail":
            results = reduce(lambda left, right: pd.merge(left, right, on=['filesize (bytes)',
                                                                           "blocksize (%)"]), df_list)


        return results

if __name__ == '__main__':
    testinstance = AlignmentRobustnessTest()
    testfile = "../../testdata/testfile_1000_random"

    algorithms = ["SSDEEP", "TLSH", "MRSHCF"]
    #results = testinstance.test(algorithms, testfile, 109749, 5000, "fixed")

    #results_tail = testinstance.test(algorithms, testfile, 500, 10, "percentage_tail")
    #print(tabulate(results_tail, headers='keys', tablefmt='psql'))
    #results_head = testinstance.test(algorithms, testfile, 500, 10, "percentage_head")
    #print(tabulate(results_head, headers='keys', tablefmt='psql'))

    directory_path = "../../testdata/testfiles_alignment_robustness"
    file_manipulation.get_random_files(directory_path, 30000, 10)
    result_list = []

    for subdir, dirs, files in os.walk(directory_path):
        for file in files:
            filepath = directory_path + "/" + file
            results_head = testinstance.test(algorithms, filepath, 500, 10, "percentage_tail")
            result_list += [results_head]

    results = reduce(pd.DataFrame.add, result_list) / len(result_list)
    print(tabulate(results, headers='keys', tablefmt='psql'))
    results.to_csv('../../results/alignment_robustness_tail_30Kb.csv')
    data = pd.read_csv('../../results/alignment_robustness_tail_30Kb.csv', index_col=0)
    plot1 = data.plot(x="blocksize (%)", y=["SSDEEP", "TLSH", "MRSHCF"])
    # plot1.invert_xaxis()
    plot1.set_ylabel("Similarity Score")
    plot1.set_xlabel("Size of added block (%)")
    plot1.set_title("Alignment Robustness Tail Test (30 KB files)")
    plt.savefig("../../results/alignment_robustness_tail_30Kb.png", dpi=300)
    plt.show()