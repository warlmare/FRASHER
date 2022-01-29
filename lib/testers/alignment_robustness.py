from base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate

class AlignmentRobustnessTest(BaseTest):

    def create_testdata(self, filepath:str, target_path:str, blocklength:int, mode:str) -> str:
        '''Creates a single testfile that has a certain amount of random bytes inserted at the beginning
        either a fixed percentage or block size

        :param filepath: the path of the file
        :param target_path: the new file will be saved to this location
        :param mode: either fixed of percentage
        :param blocklength: size either in percentages or in KB blocks

        :return: filepath to newly created file
        '''

        new_file_path = target_path + "/" + mode + "_" + str(blocklength)

        if mode == "fixed":
            new_file_byt = file_manipulation.fixed_blocks_random_head(filepath, blocklength)
        elif mode == "percentage":
            new_file_byt = file_manipulation.fixed_blocks_random_head(filepath, blocklength)

        f = open(new_file_path, "wb")
        f.write(new_file_byt)
        f.close()

        return new_file_path

    def test(self, algorithm:str, mode:str, filepath:str, max_blocklength:int, stepsize:int) -> list:
        '''alignment robustness test for a specified algorithm.

        Analyzes the impact on approximate matching when inserting byte sequences at the beginning of
        an input either of fixed size size or percentage blocks.

        :param algorithm: algorithm used for approximate matching
        :param mode: either "fixed" KB will be inserted or "percentage" blocks
        :param filepath: path of the file that will be manipualted
        :param max_blocklength: is the maximum block size that will be inserted into the file in bytes
        :param stepsize: the inserted blocks will increase by a specified amount either in percent or bytes
        :return testrun_tb: list of arrays with results, first element is headers, filesize, blocksize, blocksize %,
                            similarity score.

        '''

        testfoldername = "alignment_robustness_" + algorithm
        testfolderpath = self.create_testrun_folder(testfoldername)
        current_blocklength = 0
        current_blocklength += stepsize
        filesize = helper.getfilesize(filepath)
        

        testrun_tb = [["filesize (bytes)", "blocksize (bytes)", "blocksize (%)", "similarity score"]]
        first_testfile = self.create_testdata(filepath, testfolderpath, current_blocklength, mode)
        
        if algorithm == "tlsh":

            # TODO: this is yet only implemented for fixed blocks and needs to be implemented for percentage blocks
            testrun_tb = [["filesize (bytes)", "blocksize (bytes)", "blocksize (%)", "tlsh distance score"]]
            instance = algorithms.TLSH()
            score = instance.compare_file_against_file(filepath, first_testfile)
            blocksize_perc = round((current_blocklength / filesize) * 100, 2)
            testrun_tb.append([helper.getfilesize(first_testfile), current_blocklength, blocksize_perc, score])



            while score < 300 and current_blocklength < max_blocklength:

                current_blocklength += stepsize
                testfile = self.create_testdata(filepath, testfolderpath, current_blocklength, mode)
                score = instance.compare_file_against_file(filepath, testfile)
                blocksize_perc = round((current_blocklength / filesize) * 100, 2)
                testrun_tb.append([helper.getfilesize(first_testfile), current_blocklength, blocksize_perc, score])

            else:
                print("either the manipulated files could no longer be matched or the fragment > max_blocklength")

            return testrun_tb

        else:
            print("algorithm not yet implemented")

if __name__ == '__main__':
    testinstance = AlignmentRobustnessTest()
    testfile = "../../testdata/test_file3"
    testrun = testinstance.test("tlsh", "fixed", testfile, 64000, 5000)
    print(tabulate(testrun))
