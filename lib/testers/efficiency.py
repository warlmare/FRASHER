from base_test import BaseTest
from sys import getsizeof
from lib.helpers import helper
import timeit
import tabulate

import os

class EfficienyTest(BaseTest):

    def get_compression(self, algorithm:str, filepath) -> int:
        """Compression measures the ratio between input and output of
        an algorithm it is calculated in the following way:

        compresssion = (output length / input length) = compression

        :param algorithm: algorithm used for approximate matching
        :param filepath: path to the file that will be hashed
        :return: compression
        """

        algorithm_instance = helper.get_algorithm(algorithm)
        fuzzy_hash = algorithm_instance.get_hash(filepath)

        # some algorithms return no hashes but their hash size instead
        if type(fuzzy_hash) is int:
            output_size = fuzzy_hash
        elif(type(fuzzy_hash) is str):
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
        algorithm_instance = helper.get_algorithm(algorithm)
        fuzzy_hash = algorithm_instance.get_hash(filepath)

        # some algorithms return no hashes but their hash size instead
        if type(fuzzy_hash) is int:
            elapsed_time = timeit.timeit(
                lambda: algorithm_instance.compare_hash(filepath), number=100
            ) / 100
        elif (type(fuzzy_hash) is str):
            #execution of the hash comparison is timed 100 x times and averaged. Garbage collector is emptied prior.
            elapsed_time = timeit.timeit(
                lambda: algorithm_instance.compare_hash(fuzzy_hash, fuzzy_hash), number=100
            )/100

        return elapsed_time

    def get_runtime_efficiency(self, algorithm, filepath) -> float:
        """runtime is the time it takes the algorithm to generate
        the single hash from an input.

        :param algorithm: algorithm used for approximate matching
        :param filepath: path to the file that will be hashed
        :return: floating point seconds
        """
        algorithm_instance = helper.get_algorithm(algorithm)
        # execution of the hash generation is timed 10 x times and averaged. Garbage collector is emptied prior.
        elapsed_time = timeit.timeit(
            lambda: algorithm_instance.get_hash(filepath), number=10
        ) / 10
        return elapsed_time

    def test(self, algorithm, testfile) -> list:
        """ This test consists of a compression test, a reponse time test and a runtime efficiency test

        :param algorithm:
        :param testfile:
        :return: list of arrays with compression_value, response_time, runtime_efficiency
        """

        compression = self.get_compression(algorithm, testfile)
        response_time = self.get_response_time(algorithm, testfile)
        runtime_efficiency = self.get_runtime_efficiency(algorithm, testfile)
        testrun_tb = [["compression", "response_time", "runtime_efficiency"]]
        testrun_tb.append([compression, response_time, runtime_efficiency])
        return testrun_tb

if __name__ == '__main__':
    testfile1 = "../../testdata/test_file4.pdf"
    instance = EfficienyTest()
    testrun = instance.test("SSDEEP", testfile1)
    print(testrun)

    mrsh_test = instance.test("MRSHCF", testfile1)
    print(mrsh_test)




