from lib.hash_functions import algorithms
from base_test import BaseTest
from sys import getsizeof
from lib.helpers import helper
import importlib


class EfficienyTest(BaseTest):

    def get_compression(self, algorithm, filepath) -> int:
        """Compression measures the ratio between input and output of
        an algorithm it is calculated in the following way:

        compresssion = (output length / input length) = compression

        :param algorithm: algorithm used for approximate matching
        :param filepath: path to the file that will be hashed
        :return: compression
        """
        instance = algorithm.
        fuzzy_hash =
        output_size = getsizeof(fuzzy_hash)
        input_size = helper.getfilesize(filepath)
        compression = (output_size / input_size)
        return compression

    def get_response_time(self, algorithm, filepath) -> float:
        """ response time is the time it takes an algorithm compare
        an input hash with another hash.

        :param algorithm: algorithm used for approximate matching
        :param filepath: path to the file that will be hashed
        :return: floating point seconds
        """

    def get_runtime_efficiency(self, algorithm, filepath) -> float:
        """runtime is the time it takes the algorithm to generate
        the single hash from an input.

        :param algorithm: algorithm used for approximate matching
        :param filepath: path to the file that will be hashed
        :return: floating point seconds
        """

if __name__ == '__main__':
    testfile1 = "../../testdata/test_file3"
    instance = EfficienyTest()
    print(instance.get_compression("SSDEEP", testfile1))