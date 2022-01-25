from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate

class SingleCommonBlock(BaseTest):

    def create_testdata(self, filepath1, filepath2, target_path, filesize, chunkfile_path, chunksize) -> str:
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

        first_new_file_path = target_path + "/" + str(filesize) + "_first_file_" + str(chunksize)
        second_new_file_path = target_path + "/" + str(filesize) + "_second_file_" + str(chunksize)

        # first_new_file and second_new_file are bytestreams of the files to be written to disk
        first_new_file, second_new_file = file_manipulation.common_block_insertion(filepath1, filepath2, chunkfile_path, chunksize)

        f1 = open(first_new_file_path, "wb")
        f1.write(first_new_file)
        f1.close()

        f2 = open(second_new_file_path, "wb")
        f2.write(second_new_file)
        f2.close()

        return first_new_file_path, second_new_file_path

    def test(self, algorithm:str, filePath1:str, filePath2:str, chunkfile_path:str) -> list:
        '''realizes the single-common-block-correlation for a specific algorithm with three files that need to be
        "completely different" from one another.

        :param algorithm: the algorithm that should be tested (string)
        :param filePath1: the path of the first file that will be used for common block insertion
        :param filePath2: the path to the second file that will be used for common block insertion
        :param chunkfile_path: path to the file that will be inserted into the others

        return: list of arrays with results, first row is headers
                filesize, fragment size, fragment size %, similarity score
        '''

        # create instance of a test to create a testfolder TODO: this is rather messy and should be done through helpers
        #testinstance2 = BaseTest()


        testfoldername = "single_common_block_correlation_" + algorithm
        testfolderpath = self.create_testrun_folder(testfoldername)
        filesize = helper.getfilesize(filePath1)

        #array where all the results of the testrun are saved TODO: pull into superclass
        testrun_tb = [["filesize (bytes)", "fragment size (bytes)", "fragment size %", "similarity score"]]


        chunksize = int(filesize / 2)
        filepath1, filepath2 = self.create_testdata(filePath1, filePath2, testfolderpath, filesize, chunkfile_path, chunksize)


        if algorithm == "tlsh": # TODO: TLSH is momentarily hard-coded as it uses distance score, not similarity.
            testrun_tb = [["filesize (bytes)", "fragment size (bytes)", "fragment size %", "tlsh distance score"]]
            instance = algorithms.TLSH()
            score = instance.compare_file_against_file(filepath1, filepath2)
            while score < 300:  # TODO: research the best score threshold

                # decrease chunksize by 16000 bytes
                chunksize -= 16000


                if chunksize > 0:
                    filepath1, filepath2 = self.create_testdata(filePath1, filePath2, testfolderpath, filesize,
                                                                        chunkfile_path, chunksize)
                    score = instance.compare_file_against_file(filepath1, filepath2)
                    fragmentsize_prc = int((chunksize / filesize) * 100)
                    testrun_tb.append([filesize, chunksize, fragmentsize_prc, score])

                else:
                    print("chunksize has reached 0!")
                    break
            else:
                print("files can no longer be matched by the algorithm")

            return testrun_tb

        else:
            print("algorithm not yet implmeneted") #TODO: do a clean exception if unknown algorithm is called.



# if __name__ == '__main__':
#
#     testinstance = SingleCommonBlock()
#
#     #
#     filePath1 = "../../testdata/2048/test_file1_2048"
#     filePath2 = "../../testdata/2048/test_file2_2048"
#     chunk_filePath = "../../testdata/test_file3"
#
#     algorithm = "tlsh"
#
#     testrun = testinstance.test(algorithm, filePath1, filePath2, chunk_filePath)
#
#     print(tabulate(testrun, headers="firstrow")) #TODO: this needs to be dealt with in a log class
#
#     # for every filesize there needs to be one single_common_block_correlation_test
#     # TODO: needs to be realized for the filesizes = [512,2048,8192] for each filesize 5 runs and the values are averaged











