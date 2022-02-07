import os

import ssdeep

import nltk
import tlsh

nltk.download('punkt')
from simhash import Simhash
import subprocess
import re
import math
import time
from  lib.helpers import helper
import os
import errno
import pathlib
import pprint


# TODO: Function that pulls all the algorithms/ checks their conditions and their checkups

class Algorithm:


    # TODO: create a output_cleaner-method that cleans up the output of every algorithm

    def compare_t5_file_against_itself_console(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_t5_file_against_itself_string(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_t5_file_against_filter(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_t5file_against_t5file(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def create_filter(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_file_against_file(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_filte_against_filer(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def tokenizer(string):
        tokens = nltk.word_tokenize(string)
        return tokens

    # TODO: so sorry, this needs to be purged.
    def file_sizes(self, file):
        t5_file = file
        output = os.popen("wc -c {} ".format(t5_file)).read()
        return output


class TextAlgorithm:

    def compare_text_against_text(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_text_against_test_string(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def compare_file_against_file(self, *args):
        raise NotImplementedError("Subclass must implement abstract method")

    def reading_a_file(filepath):
        text = open(filepath).read()
        return text


class SSDEEP(Algorithm):

    def compare_file_against_file(self, file_a, file_b):
        hash1 = ssdeep.hash_from_file(file_a)
        hash2 = ssdeep.hash_from_file(file_b)
        score = ssdeep.compare(hash1, hash2)
        return score

    def get_hash(self, filepath: str) -> str:
        """
        generates a hash from a file

        :param filepath: path to the file that will be hashed
        :return: hash as string
        """
        fuzzy_hash = ssdeep.hash_from_file(filepath)
        return fuzzy_hash

    def compare_hash(self, hash1: str, hash2: str) -> int:
        """
        compares two hash strings

        :param hash1:
        :param hash2:
        :return: similarity score
        """
        score = ssdeep.compare(hash1, hash2)
        return score

    def get_filter(self, directory_path:str) -> dict:
        '''fills a list with all the hashes of files from a folder

        :param folderpath: path to the folder with files
        :return: dictionary with filename:hash pairs
        '''

        hash_filter = {}

        try:
            os.path.isdir(directory_path)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), directory_path)
        else:
            for subdir, dirs, files in os.walk(directory_path):
                for file in files:
                    filename = os.fsdecode(file)
                    filepath = os.path.join(directory_path, file)
                    hash = self.get_hash(filepath)
                    hash_filter[filename] = hash

        return hash_filter

    def compare_file_against_filter(self, filter:dict, filepath) ->dict:
        '''compares a single hash with every hash in a filter
        in O(1). (iteratively)

        :param filter: list [[filename, hash], [..., ...], ... ]
        :param filepath:
        :return: dictionary with filename : score
        '''

        file_hash = ssdeep.hash_from_file(filepath)
        results = {}

        for filename, filter_hash in filter.items():
            score = self.compare_hash(file_hash, filter_hash)
            results[filename] = score

        return results

class TLSH(Algorithm):
    def get_hash(self, filepath: str) -> str:
        """
        generates a hash from a file

        :param filepath: path to the file that will be hashed
        :return: hash as string
        """
        fuzzy_hash = tlsh.Tlsh()
        with open(filepath, 'rb') as f:
            for buf in iter(lambda: f.read(512), b''):
                fuzzy_hash.update(buf)
            fuzzy_hash.final()

        fuzzy_hash = fuzzy_hash.hexdigest()
        return fuzzy_hash


    def compare_hash(self, hash1: str, hash2: str) -> int:
        """
        compares two hash strings

        :param hash1:
        :param hash2:
        :return: similarity score from 0 - 100; 100 beeing identical
        """
        score = tlsh.diff(hash1, hash2)

        if score > 300:  # We consider 300 to be the cutoff value at which files can no longer be matched
            result = 0
        else:
            # TLSH's score: the lower the more similar - we readjust that value on a scale from 0-100. 0 beeing 0 similarity
            result = 100 - ((score * 1 / 300) * 100)

        return result


    def get_filter(self, directory_path:str) -> dict:
        '''fills a list with all the hashes of files from a folder

        :param folderpath: path to the folder with files
        :return: dictionary with filename:hash pairs
        '''

        hash_filter = {}

        try:
            os.path.isdir(directory_path)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), directory_path)
        else:
            for subdir, dirs, files in os.walk(directory_path):
                for file in files:
                    filename = os.fsdecode(file)
                    filepath = os.path.join(directory_path, file)
                    hash = self.get_hash(filepath)
                    hash_filter[filename] = hash

        return hash_filter

    def compare_file_against_filter(self, filter:dict, filepath) -> dict:
        '''compares a single hash with every hash in a filter
        in O(1). (iteratively)

        :param filter: list [[filename, hash], [..., ...], ... ]
        :param filepath:
        :return: dictionary with filename : score
        '''

        file_hash = self.get_hash(filepath)
        results = {}

        for filename, filter_hash in filter.items():
            score = self.compare_hash(file_hash, filter_hash)
            results[filename] = score

        return results

    def compare_t5_file_against_itself_console(self, file):
        file_path = './t5/{}'.format(file)
        data1 = tlsh.Tlsh()
        with open(file_path, 'rb') as f:
            for buf in iter(lambda: f.read(512), b''):
                data1.update(buf)
            data1.final()
        score = data1.diff(data1)
        print(score)

    def compare_t5_file_against_itself_string(self, file):
        file_path = './t5/{}'.format(file)
        data1 = tlsh.Tlsh()
        with open(file_path, 'rb') as f:
            for buf in iter(lambda: f.read(512), b''):
                data1.update(buf)
            data1.final()
        score = data1.diff(data1)
        return str(score)

    def create_filter(self, folder):
        os.system("ALGORITHMEN/tlsh/tlsh  -r {} >  FILTER/tlsh_filter ".format(folder))

    def tlsh_output_cleaner_file_against_filter(self, output_string):
        # The mrshcf output follows the following format when compar a file against itself:  Filter Generation time is1.61256e+09 seconds . ./t5/000012.pdf      Total Chunks: 54	 Chunks Detected: 54
        output_format = ['original_file', 'filename', 'chunks_detected']
        output_tokenized = Algorithm.tokenizer(str(output_string))
        output_clean = dict(zip(output_format, output_tokenized))
        return output_clean

    # deprecated
    def compare_file_against_filter_debug(self, file):
        # os.system("./Algorithms/tlsh/bin/tlsh -c t5/{} -l t5Filter ".format(file))
        t5_file = file
        res = subprocess.run(
            ["ALGORITHMEN/tlsh/tlsh", "-c", t5_file, "-l", "FILTER/tlsh_filter"],
            stdout=subprocess.PIPE,
            universal_newlines=True).stdout

        thing = ""

        tfw = iter(res.splitlines())
        for line in tfw:
            if re.search(r"(?<!\d)[0-1]\d{0,2}(?!\d)$", line):
                filename = str(self.tlsh_output_cleaner_file_against_filter(line).get("filename")).replace("t5//",
                                                                                                           "t5/", 1)
                chunks_detected = str(self.tlsh_output_cleaner_file_against_filter(line).get("chunks_detected"))
                total_chunks = str(os.path.getsize(filename))
                chunks_detected_in_prc = str(math.trunc((round(1000 - int(chunks_detected)) * 0.1)))
                thing += filename + ",      Total Chunks:  100,     Chunks Detected: " + chunks_detected_in_prc + "\n"

        return thing


    def compare_file_against_file(self, file1, file2):

        data1 = tlsh.Tlsh()
        data2 = tlsh.Tlsh()

        with open(file1, 'rb') as f:
            for buf in iter(lambda: f.read(512), b''):
                data1.update(buf)
            data1.final()

        with open(file2, 'rb') as f:
            for buf in iter(lambda: f.read(512), b''):
                data2.update(buf)
            data2.final()

        score = data1.diff(data2)
        if score > 300: #We consider 300 to be the cutoff value at which files can no longer be matched
            result = 0
        else:
            #TLSH's score: the lower the more similar - we readjust that value on a scale from 0-100. 0 beeing 0 similarity
            result = 100 - ((score * 1/300) * 100)

        return result


class SiSe(Algorithm):

    def compare_t5_file_against_itself_console(self, file):
        os.system("./ALGORITHMEN/sise -c t5/{} t5/{}".format(file, file))

    def compare_t5_file_against_itself_string(self, file):
        output = os.popen("../ALGORITHMEN/sise -c t5/{} t5/{}".format(file, file)).read()
        return output

    # TODO: compare file against filter

    def compare_t5file_against_t5file(self, file1, file2):
        os.system("./ALGORITHMEN/sise -c t5/{} t5/{}".format(file1, file2))


class MrshHbft(Algorithm):
    # TODO: variations in the leafsize blocksize and min_runs should be explained

    def compare_t5_file_against_itself_console(self, file):
        os.system("./ALGORITHMEN/mrsh_hbft t5/{} t5/{} 160 1 1".format(file, file))

    # TODO: before any toeknization can happen the output of the algorithm has to be changed.
    def compare_t5_file_against_itself(self, file):
        output = os.popen("./ALGORITHMEN/mrsh_hbft t5/{} t5/{} 160 1 1".format(file, file))
        return output

    def compare_t5file_against_t5file_console(self, file1, file2):
        os.system("./ALGORITHMEN/mrsh_hbft t5/{} t5/{} 160 4 3".format(file1, file2))

    # TODO def compare_file_against_filter


class Jsdhash(Algorithm):

    def compare_t5_file_against_itself_console(self, file):
        os.system("./ALGORITHMEN/J-sdhash -g t5/{} t5/{}".format(file, file))

    def compare_t5_file_against_itself_string(self, file):
        output = os.popen("./ALGORITHMEN/J-sdhash -g t5/{} t5/{}".format(file, file))
        return output

    def compare_t5file_against_t5file(self, file1, file2):
        os.system("./ALGORITHMEN/J-sdhash -g t5/{} t5/{}".format(file1, file2))

    def generater_filter(self, filter):
        os.system("./ALGORITHMEN/J-sdhash -r  t5/{} > J-sdhash_filter".format(filter))


class Sdhash(Algorithm):

    def compare_t5_file_against_itself_console(self, file):
        os.system("./ALGORITHMEN/sdhash -g t5/{} t5/{}".format(file, file))

    def compare_t5_file_against_itself_string(self, file):
        output = os.popen("./ALGORITHMEN/sdhash -g t5/{} t5/{}".format(file, file))
        return output

    def compare_t5file_against_t5file(self, file1, file2):
        os.system("./ALGORITHMEN/sdhash -g t5/{} t5/{}".format(file1, file2))

    # TODO def compare_file_against_filter


class SimHash(TextAlgorithm):

    def compare_text_against_text(self, text1, text2):
        simhash_result = int(Simhash(text1).distance(Simhash(text2)))
        simhash_in_perc = 100 - simhash_result
        result = str(simhash_in_perc)
        return result

    def compare_text_against_text_string(self, text1, text2):
        output = os.popen("SimHash distance: " + str(Simhash(text1).distance(Simhash(text2))))
        return output

    def compare_two_files(self, filename1, filename2):
        text1 = TextAlgorithm.reading_a_file(filename1)
        text2 = TextAlgorithm.reading_a_file(filename2)
        simhash_output = self.compare_text_against_text(text1, text2)
        output = simhash_output
        return output

    def compare_file_against_folder(self, filename1, folderpath):
        list = "filename,filesize,payloadsize,chunks_detected,chunks_total\n"
        file_truncated = os.path.basename(filename1)
        filepath_orig = '{}'.format(filename1)
        filepath_new = '{}'.format(filename1)
        file_size_orig = str(os.path.getsize(filepath_orig))  # os.popen("wc -c {} ".format(filepath_orig)).read()
        file_size_new = str(os.path.getsize(filepath_new))  # os.popen("wc -c {} ".format(filepath_new)).read()
        file_size_new_prc = str(math.trunc(round((int(file_size_new) / int(file_size_orig)) * 100)))
        for file in os.listdir(folderpath):
            filepath = str(folderpath + file)
            file_size_compared_file = str(os.path.getsize(filepath))  # os.popen("wc -c {} ".format(filepath)).read()
            simhash_output_str = self.compare_two_files(filename1, filepath)
            if file_truncated == file:
                output_str = ("{},{},{},{},100\n".format(filepath, file_size_compared_file, file_size_new_prc,
                                                         simhash_output_str))
                list += output_str
            else:
                output_str = ("{},{},,{},100\n".format(filepath, file_size_compared_file, simhash_output_str))
                list += output_str
        return list


class MRSHCF(Algorithm):


    def compare_file_against_file(self, file1, file2) -> int:
        '''compares two files and returns the similarity score (Chunks Detected / Total Chunks)

        :param file1: filepath
        :param file2: filepath
        :return: sim_score (Chunks Detected / Total Chunks) * 100 -> pre-decimal points
        '''

        comparison_output = self.compare_file_against_file_tokenized(file1, file2)
        chunks_total = comparison_output.get("total_chunks")
        chunks_detected = comparison_output.get("chunks_detected")

        #TODO: mrsh-cf might depend heavily depend on decimal places so change this to include decimal points
        sim_score = (int(chunks_detected) / int(chunks_total)) * 100
        return sim_score

    def compare_file_against_file_console(self, file1, file2):
        '''compares two files and returns the command line output

        :param file1: filepath
        :param file2: filepath
        '''
        os.system("./mrsh-cf/mrsh_cuckoo.exe -f {} -c {}".format(file1, file2))


    def get_hash(self, filepath) -> float:
        '''generates a hash from a file in a filter form
        mrsh cannot return the hash in string form but returns the size of the hash / filter

        :param filepath:
        :return: filter size in bytes
        '''
        # TODO: this needs to be set for the whole file
        os.chdir("/home/frieder/FRASH2_0/lib/hash_functions")
        os.system("./mrsh-cf/mrsh_cuckoo.exe -f {} -g".format(filepath))
        hash_size = helper.getfilesize("./mrsh-cf/mrsh.sig")
        return hash_size

    def compare_hash(self, filepath):
        '''
        compares a hash against a hash
        since mrsh-cf gives no access to its methods we compare a file with itself

        :param filepath:
        '''
        #TODO: output needs to be surpressed in some form
        placeholder = self.compare_file_against_file_console(filepath, filepath)

    def compare_file_against_file_tokenized(self, file1, file2):
        os.chdir("/home/frieder/FRASH2_0/lib/hash_functions")
        output_raw = subprocess.getoutput("./mrsh-cf/mrsh_cuckoo.exe -f {} -c {}".format(file1, file2))
        output = self.output_cleaner_file_vs_file(output_raw)
        return output

    # deprecated
    def output_cleaner(self, output_string):
        # The mrshcf output follows the following format when compar a file against itself:  Filter Generation time is1.61256e+09 seconds . ./t5/000012.pdf      Total Chunks: 54	 Chunks Detected: 54
        output_format = ['inputfile',
                         'Total', 'Chunks', 'Doublepoint', 'total_chunks', 'Chunks', "Detected", "Doublepoint",
                         'chunks_detected']
        output_tokenized = Algorithm.tokenizer(str(output_string))
        output_clean = dict(zip(output_format, output_tokenized))
        return output_clean

    def output_cleaner_file_vs_file(self, output_string):
        # The mrshcf output follows the following format when compar a file against itself:  Filter Generation time is1.61256e+09 seconds . ./t5/000012.pdf      Total Chunks: 54	 Chunks Detected: 54
        output_format = ['Filter', 'Generation', 'Time', 'filtergenerationtime', 'Seconds', 'Point', 'inputfile',
                         'Total', 'Chunks', 'Doublepoint', 'total_chunks', 'Chunks', "Detected", "Doublepoint",
                         'chunks_detected']
        output_tokenized = Algorithm.tokenizer(str(output_string))
        output_clean = dict(zip(output_format, output_tokenized))
        return output_clean

    def compare_t5_file_against_itself_tokenized(self, file):
        output_raw = subprocess.getoutput("./ALGORITHMEN/mrsh_cuckoo.exe -f ./t5/{} -c ./t5/{}".format(file, file))
        output = self.output_cleaner(output_raw)
        return output



    # compares a file from the t5-filter against a filter of all t5 files
    def compare_t5_file_against_filter_console(self, file):
        os.system("./ALGORITHMEN/mrsh_cuckoo.exe -s ./t5 -c ./t5/{}".format(file))

    def output_cleaner_file_against_filter(self, output_string):
        # The mrshcf output follows the following format when compar a file against itself:  Filter Generation time is1.61256e+09 seconds . ./t5/000012.pdf      Total Chunks: 54	 Chunks Detected: 54
        output_format = ['inputfile', 'total_chunks', 'chunks_detected']
        output_tokenized = Algorithm.tokenizer(str(output_string))
        output_clean = dict(zip(output_format, output_tokenized))
        return output_clean

    # compares a file from the t5-filter against a filter of all t5 files
    def compare_t5_file_against_filter_tokenized(self, file):
        output_raw = subprocess.getoutput("./ALGORITHMEN/mrsh_cuckoo.exe -s ./t5 -c ./t5/{}".format(file))
        output = self.output_cleaner_file_against_filter(output_raw)
        return output

    def output_cleaner_file_against_filter2(self, output_string):
        # The mrshcf output follows the following format when compar a file against itself:  Filter Generation time is1.61256e+09 seconds . ./t5/000012.pdf      Total Chunks: 54	 Chunks Detected: 54
        output_format = ['inputfile', ]
        output_tokenized = Algorithm.tokenizer(str(output_string))
        output_clean = dict(zip(output_format, output_tokenized))
        return output_clean

    def compare_file_against_folder_console_debug(self, file, folder):
        t5_file = file
        res = subprocess.run(
            ["./ALGORITHMEN/mrsh_cuckoo.exe", "-f", t5_file, "-c", folder],
            # ["./mrsh_cuckoo.exe", "-s", "t5/", "-c", t5_file ],
            stdout=subprocess.PIPE,
            universal_newlines=True).stdout

        thing = ""

        tfw = iter(res.splitlines())
        for line in tfw:
            # print(line)
            filename = str(self.output_cleaner_file_against_filter(line).get("inputfile"))
            chunks_detected = str(self.output_cleaner_file_against_filter(line).get("chunks_detected"))
            total_chunks = str(self.output_cleaner_file_against_filter(line).get("total_chunks"))
            chunks_detected_in_prc = str(math.trunc(round((int(chunks_detected) / int(total_chunks)) * 100)))
            thing += filename + ",      Total Chunks:  100,     Chunks Detected: " + chunks_detected_in_prc + "\n"

        return thing


if __name__ == '__main__':
    filePath1 = "../../testdata/test_file5"
    filePath2 = "../../testdata/test_file5_short"
    chunk_filePath = "../../testdata/test_file3"

    #ssdeep_instance = SSDEEP()
    #ssdeep_instance.compare_file_against_file(filePath1, filePath2)
    #filter  = ssdeep_instance.get_filter("../../testdata")
    #res  = ssdeep_instance.compare_file_against_filter(filter, filePath1)
    #pprint.pprint(res)

    tlsh_instance = TLSH()
    filter = tlsh_instance.get_filter("../../../t5")
    tlsh_instance.compare_file_against_filter(filter, filePath2)






