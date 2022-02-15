import os, glob
import random
from random import shuffle
from base_test import BaseTest
from lib.helpers import helper
from lib.helpers import file_manipulation
from lib.hash_functions import algorithms

class NIHTestCrossCorrelation(BaseTest):

    def test(self, directory_path):
        ''' TODO: explain

        :param directory_path:
        :param target_path:
        :return: filelist

        '''

        files = os.listdir(directory_path)
        extensions = helper.get_extensions_in_dir(directory_path)
        needle_directory_name = "needle_in_the_haystack_cross_correlation"
        needle_directory_path = self.create_testrun_folder(needle_directory_name)


        for ext in extensions:
            print(ext)
            # all files with certain extension
            files_with_ext = [i for i in files if ext in i]
            sample = random.sample(files_with_ext, 10)
            sample_paths = []

            #creates the full paths to the files
            for file in sample:
                sample_paths.append(os.path.join(directory_path, file))

            shuffle(sample_paths) # TODO: This ought to be solved with structs to stop reocurrences
            sample_file_a = sample_paths[0]
            sample_file_b = sample_paths[1]

            sample_file_a_orig_name = helper.get_file_name(sample_file_a)
            sample_file_b_orig_name = helper.get_file_name(sample_file_b)

            sample_file_a_filesize = helper.getfilesize(sample_file_a)
            sample_file_a_chunksize = (sample_file_a_filesize / 2)


            needle_a_path = needle_directory_path + "needle_a_" + sample_file_a_orig_name
            needle_b_path = needle_directory_path + "needle_b_" + sample_file_b_orig_name

            if ext == ".gif":
                chunk = helper.get_rand_chunk_of_ext(".gif",sample_file_a_chunksize)
                needle_a, needle_b = file_manipulation.common_block_insertion_byt(sample_file_a,
                                                                                  sample_file_b,
                                                                                  chunk)
                f = open(needle_a_path , "wb")
                f.write(needle_a)
                f.close()

                f = open(needle_b_path , "wb")
                f.write(needle_b)
                f.close()

            elif ext == ".text":

            elif ext == ".jpg":

            elif ext == ".doc":

            elif ext == ".xls":

            elif ext == ".html":

            elif ext == ".ppt":

            elif ext == ".pdf":


if __name__ == '__main__':
    dir = "../../../t5"
    test_instance = NIHTestCrossCorrelation()
    test_instance.test(dir, "sdlkfjsldkfj")