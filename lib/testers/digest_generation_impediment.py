from lib.testers.base_test import BaseTest
from lib.helpers import file_manipulation
from lib.helpers import helper
from lib.hash_functions import algorithms
from tabulate import tabulate

import pandas as pd
import re
from functools import reduce
from random import randint
import matplotlib.pyplot as plt
import os

import random
import string
import tlsh
import nltk
nltk.download('words')
from nltk.corpus import words
from random import sample
from lorem.text import TextLorem

dirname = os.path.dirname(__file__)

class DigestGenerationImpediment(BaseTest):


    # TODO: move to lib.helpers
    def percentage(self, part, whole):
        percentage = float(whole * 0.01) * float(part)
        return int(percentage)

    # TODO: move into lib.helpers
    def get_ran_seq(self, sequence_length, alphabet_length):
        # 100 ascii chars
        alphabet = string.printable # "".join(chr(i) for i in range(128)) #
        body_chars = alphabet[0:alphabet_length]
        print(body_chars)
        sequence = ''

        while len(set(sequence)) is not len(body_chars):
            sequence = ''.join(random.SystemRandom().choice(body_chars) for _ in range(sequence_length))


        seq_bytes = sequence #.encode("utf-8")
        return seq_bytes

    def get_ran_text(self, text_len, dict_size):

        orig_dict = words.words()
        word_gen = list(filter(lambda i: len(i)==2, orig_dict))
        dictionary = ' '.join(sample(word_gen, dict_size))

        lorem = TextLorem(wsep=' ', srange=(text_len -1, text_len), words=dictionary.split())

        g = lorem.sentence()
        sequence = g.encode("utf-8")

        return sequence

    def test(self, algorithms):
        '''generates a random string sequence from 100 unique ASCII chars
        of size 1KB. Turn after turn the number of unique chars is lowered
        whilst the string length stays the same. The algorithms have to
        hash the random sequence. This way it is revealed wether a fuzzy
        hash can deal with an input with low variance.

        :param args:
        :return:
        '''

        sequence_length = 2900

        df_list = []
        sequence_a = os.path.join(dirname,"/home/frieder/FRASH2_0/lib/testers/sequence_a")
        sequence_b = os.path.join(dirname, "/home/frieder/FRASH2_0/lib/testers/sequence_b")

        for i in algorithms:
            algorithm_instance = helper.get_algorithm(i)
            testrun_tb = [["variance",i]]

            for variance in range(100):
                sequence_a_content = self.get_ran_seq(sequence_length,variance)# get_ran_text(sequence_length,variance)#
                with open(sequence_a, "w") as text_file:
                    text_file.write(sequence_a_content)
                text_file.close()

                print(helper.getfilesize(sequence_a))

                sequence_b_content = self.get_ran_seq(sequence_length,variance)#get_ran_text(sequence_length,variance)##
                with open(sequence_b, "w") as text_file:
                    text_file.write(sequence_b_content)
                text_file.close()

                try:
                    sim_score = algorithm_instance.compare_file_against_file(sequence_a,
                                                                             sequence_a)
                    print(sim_score)
                # if the sim_score is anything other than 0 this is considered a sucess (1) otherwise (0)
                except ValueError as error:
                    testrun_tb.append([variance,"0"])
                else:
                    if sim_score == 0:
                        testrun_tb.append([variance, "0"])
                    else:
                        testrun_tb.append([variance, "1"])

            res_df = helper.get_dataframe(testrun_tb)
            print(tabulate(res_df, headers='keys', tablefmt='psql'))
            df_list += [res_df]


        results = reduce(lambda left, right: pd.merge(left, right, on=["variance"]), df_list)
        return results

if __name__ == '__main__':
    algorithms =  ["MRSHV2"]#, "SDHASH"]#, "FBHASH"] #["SSDEEP", "TLSH", "MRSHCF", "MRSHV2", "SDHASH", "FBHASH"]

    testinstance = DigestGenerationImpediment()
    #algorithm_instance = helper.get_algorithm("SDHASH")
    results = testinstance.test(algorithms)
    print(tabulate(results, headers='keys', tablefmt='psql'))
    results.to_csv(os.path.join(dirname, '../../results/digest_generation_impediment.csv'))










