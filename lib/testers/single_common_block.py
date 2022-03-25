from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate
import re
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
import seaborn as sns


class SingleCommonBlock(BaseTest):


    def create_testdata(self, filepath1, filepath2, target_path, chunkfile_path) -> str:
        ''' Takes two files and inserts a common block of size X and saves them on disk

        :param filepath1: path to file that will be inserted with a common block.
        :param filepath2: path to file that will be inserted with a common block.
        :param target_path: here the created testfiles will be saved
        :param filesize: string that tells the size of the input files
        :param chunkfile_path: path to the file that will be inserted into both the files as a common block
        :param chunkfile_size:  size of the common element to be inserted in the files in KB

        :return: filepath1, filepath2 the paths to the new  files that were manipulated accordingly

        TODO: describe in detail how the files are beeing named (filesize, A or B, chunksize)
        '''

        # TODO: check if filesize of both files is equal
        filesize = helper.getfilesize(filepath1)
        chunksize = int(filesize / 2)
        filepaths = []
        chunk_byt = file_manipulation.getrandchunk(chunk_filePath, chunksize)#random_byte_generation(chunksize)


        while chunksize > 0:
            if chunksize <= 16000:
                chunksize -= 100
            else:
                chunksize -= 16000

            #The chunk byte is cut off at the end turn after turn ...
            chunk_byt = chunk_byt[:chunksize]
            first_new_file_path = target_path + "/_first_file_" + str(chunksize)
            second_new_file_path = target_path + "/_second_file_" + str(chunksize)

            # first_new_file and second_new_file are bytestreams of the files to be written to disk
            first_new_file, second_new_file = file_manipulation.common_block_insertion_byt(
                filepath1,
                filepath2,
                chunk_byt
                #chunkfile_path,
                #chunksize
            )


            f1 = open(first_new_file_path, "wb")
            f1.write(first_new_file)
            f1.close()

            f2 = open(second_new_file_path, "wb")
            f2.write(second_new_file)
            f2.close()

            filepaths += [[first_new_file_path, second_new_file_path]]

        return filepaths


    def test(self, algorithms:list, filepath1:str, filepath2:str, chunkfile_path:str) -> list:
        '''realizes the single-common-block-correlation for a specific algorithm with three files that need to be
        "completely different" from one another.

        :param algorithms: the algorithms that should be tested; list with strings.
        :param filePath1: the path of the first file that will be used for common block insertion
        :param filePath2: the path to the second file that will be used for common block insertion
        :param chunkfile_path: path to the file that will be inserted into the others

        return: list of arrays with results, first row is headers
                filesize, fragment size, fragment size %, similarity score
        '''

        testfoldername = "single_common_block_correlation"
        testfolderpath = self.create_testrun_folder(testfoldername)
        filesize = helper.getfilesize(filePath1)

        # [[first_file_x,second_file_x],[first_file_y, first_file_y]...]
        file_list = self.create_testdata(filepath1, filepath2, testfolderpath, chunkfile_path)


        df_list = []

        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)

            # array that saves our results
            testrun_tb = [["filesize (bytes)", "fragment size (bytes)", "fragment size %", i]]

            for elem in file_list: #[first_file_path, second_file_path]
                first_file = elem[0]
                second_file = elem[1]

                filesize = helper.getfilesize(first_file)
                scores = []
                # test are performed 5 times and averaged
                for x in range(5):
                    scores += [algorithm_instance.compare_file_against_file(
                                                                            first_file,
                                                                            second_file)]
                score = sum(scores) / len(scores)


                #takes the suffix of the testfiles
                chunksize = int(re.sub('.*?([0-9]*)$',r'\1',first_file))
                fragmentsize_prc =  (chunksize / filesize) * 100
                testrun_tb.append([filesize, chunksize, fragmentsize_prc, score])

            res_df = helper.get_dataframe(testrun_tb)
            df_list += [res_df]

        results = reduce(lambda left, right: pd.merge(left, right, on=['filesize (bytes)',
                                                                       "fragment size (bytes)",
                                                                       "fragment size %"]), df_list)
        return results


if __name__ == '__main__':

    testinstance = SingleCommonBlock()


    filePath1 = "../../testdata/8192/test_file1_8192"
    filePath2 = "../../testdata/8192/test_file2_8192"
    chunk_filePath = "../../testdata/testfile1"

    # for every filesize there needs to be one single_common_block_correlation_test
    # TODO: needs to be realized for the filesizes = [512,2048,8192] for each filesize 5 runs and the values are averaged

    algorithms = ["SSDEEP","TLSH", "MRSHCF", "SDHASH"]
    results = testinstance.test(algorithms, filePath1, filePath2, chunk_filePath)
    print(tabulate(results, headers='keys', tablefmt='psql'))
    results.to_csv('../../results/single_common_block_8192.csv')

    data = pd.read_csv('../../results/single_common_block_8192.csv', index_col=0)
    data["fragment size (bytes)"] = data["fragment size (bytes)"].div(1000)
    plot1 = data.plot(x="fragment size (bytes)", y=["SSDEEP", "TLSH", "MRSHCF", "SDHASH"])
    plot1.invert_xaxis()
    plot1.set_ylabel("Similarity Score")
    plot1.set_xlabel("Fragment Size (KB)")
    plot1.set_title("Single Common Block Test (8192)")
    plt.savefig("../../results/single_common_block_test_8192.png" , dpi=300)
    plt.show()





