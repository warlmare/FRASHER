import os

import ssdeep

import nltk
import tlsh

#nltk.download('punkt')
from simhash import Simhash
import subprocess
import re
import math


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

    #TODO: so sorry, this needs to be purged.
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


    # TODO: implement SSDEEP connection
class SSDEEP(Algorithm):
   def compare_file_against_file(self, file_a, file_b):
        hash1 = ssdeep.hash_from_file(file_a)
        hash2 = ssdeep.hash_from_file(file_b)
        score = ssdeep.compare(hash1, hash2)
        print(score)


class TLSH(Algorithm):
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

    def compare_file_against_filter(self, file):
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

        # print(self.tlsh_output_cleaner_file_against_filter(line))

    #TODO: the output must be changed since TLSH has a distnce score not a similarity score.
    def compare_file_against_file(self, file1, file2):
        #file1_path = './t5/{}'.format(file1)
        #file2_path = './t5/{}'.format(file2)
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
        #print('tlsh({}, {}): '.format(file1, file2) + str(score))
        return score


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


class MrshCf(Algorithm):

    def compare_t5_file_against_itself_console(self, file):
        os.system("./ALGORITHMEN/mrsh_cuckoo.exe -f ./t5/{} -c ./t5/{}".format(file, file))

    # makes the output readable and adressable
    def output_cleaner(self, output_string):
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

    def compare_t5file_against_t5file_tokenized(self, file1, file2):
        output_raw = subprocess.getoutput("./ALGORITHMEN/mrsh_cuckoo.exe-f ./t5/{} -c ./t5/{}".format(file1, file2))
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
    filePath1 = "../../testdata/2048/test_file1_2048"
    filePath2 = "../../testdata/2048/test_file2_2048"
    chunk_filePath = "../../testdata/test_file3"

    ssdeep_instance = SSDEEP()
    ssdeep_instance.compare_file_against_file( filePath1, filePath2)