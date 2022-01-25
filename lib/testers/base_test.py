import os
from lib.helpers import helper
from lib.hash_functions import algorithms

class BaseTest:


    def create_testdata(self, *args):
        '''creates the testdata and saves them in a specified folder

        :param args: TODO: abstract args
        '''
        raise NotImplementedError("Subclass must implement abstract method")

    def test(self, *args):
        # TODO: explain
        raise NotImplementedError("Subclass must implement abstract method")

    def result(self, *args):
        # TODO: explain
        raise NotImplementedError

    def create_testrun_folder(self, testname):
        '''creates individual testrunfolders with datetime stamp

        :param testname:

        :return: the path of the newly created folder

        :raise: OSERROR if folder cannot be created
        '''

        timestr = helper.gettimestring()
        foldername = timestr + "_" + testname
        path = "../../testdata/" + foldername

        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        return path

    def manipulation_log_update(self,log1:list, log2:list) -> list:
        ''' merges a list (log1) that contains the changes applied to a file
            with a list that holds the current state (log2).

        log1 has the syntax: [...,
                             ["del", deletion_offset, deletion_end_offset],
                             ["sub", substitution_offset, substitution_end_offset],
                             ["ins", insertion_offset, insertion_end_offset],
                             ...]


        log2 has the syntax: [filesize,
                                [[substitution_start_offset, substitution_end_offset],...],
                                [[insertion_start_offset, insertion_end_offset],...]
                             ]

        :param log1:  log1; the changes sequentially in the order they occurred
        :param log2:  current file state
        :return: log_merged
        '''

        # iterate through the log1 file and update log2 with the information
        for i in log1: #TODO: iteration doesn'T work correctly but i guess that can be fixed

            if i[0] == "del":
                # update filesize whenever bytes are deleted
                log2[0] -= int(i[2] - i[1])

                new_entry = [[i[1],i[2]]]
                # delete any overlapping tuple and update in subsituted tuples list
                log2[1] = helper.delete_overlapping_tuples_reindex(log2[1], new_entry)

                # delete any overlapping tuple and update in inserted tuples list
                log2[2] = helper.delete_overlapping_tuples_reindex(log2[2], new_entry)

            elif i[0] == "sub":
            # merge with list of other substitution offset tuples ...
                new_entry = [[i[1],i[2]]]
                log2[1].extend(new_entry) #
                # ... find any overlapping offset tuples and update the list
                log2[1] = helper.merge_overlapping_tuples(log2[1])

                #TODO: update the insertion list.

            elif i[0] == "ins":
                log2[0] += i[2] - i[1]

                new_entry = [[i[1],i[2]]]
                log2[2] = helper.insert_reindex(log2[2], new_entry)
                # delete insert tuple and update in subsituted tuples list
                log2[1] = helper.placebo_insert_reindex(log2[1], new_entry)
        
        #substituted segments and inserted segments are merged if adjacent  [4,8][8,9] = [4,9]
        subsituted = log2[1]
        inserted   = log2[2]

        log2[1] = helper.merge_adjacent_tuples(subsituted[:1], subsituted[1:])
        log2[2] = helper.merge_adjacent_tuples(inserted[:1], inserted[1:])
                
        return log2


    def get_log_arr(self, log:list) -> list:
        '''transforms a manipulation log state into a list  that represents the file state

        :param  log has the syntax: [filesize,
                                [[substitution_start_offset, substitution_end_offset],...],
                                [[insertion_start_offset, insertion_end_offset],...]
                             ]

        :return: list that represents the file state |

            [15,
                [[1,2],[6,8]],
                [[10,11],[13,14]]
            ]

            ---> [[], [], [], ..... ]

        '''

        filesize = log[0]
        a = log[1]
        b = log[2]
        list1 = (a + b)
        list2 = helper.merge_adjacent_tuples(list1[:1],list1[1:])
        print(list2)

        missing_segments = helper.get_missing(list2, 0, filesize)
        # all the missing (unchanged) segments get a boolean marker so the can be registered as unchanged
        for i in missing_segments:
            i.append(False)

        # all the changed segments get a boolean marker so the can be registered as changed
        for i in list1:
            i.append(True)

        total_segments = list1 + missing_segments

        # sort the list by the first elemnt
        total_segments.sort(key=lambda s:s[1])
        # sort the list by the second element
        total_segments.sort(key=lambda i:i[0])

        return total_segments

    def get_log_scale(self, lst):

        filelength = 0

        for ele in lst:
            start = ele[0]
            stop = ele[1]
            length = stop - start
            state = ele[2]
            filelength += length
            scaled_bar =[]

            if state is True:
                scaled_bar.append(length * 1, )
            else:
                scaled_bar.append(length * 0, )

        single_unit = filelength / 100

        #for i in scaled_bar:
        #    if i == len(i) * i[0]:



    def log_printer(self, lst:list):
        '''
        takes a list of ["111", "000", ... ] that represents which bytes in a file have been changed and prints a log

        :param lst:
        '''

        state_bar = ""

        for ele in lst:
            start = ele[0]
            stop = ele[1]
            length = stop - start
            state = ele[2]

            if state is True:
                state_bar += length * "█"
            else:
                state_bar += length * "▒"

        print(state_bar)#, end="\r", flush=True)


if __name__ == '__main__':

    log1_test = [['sub', 8, 10],['ins', 11, 13],['del', 2, 4]]
    log2_test = [30,[[0, 5], [9, 15]], [[6,8], [15, 20]]]
    log3_test = [30,[], []]

    instance = BaseTest()

    updated_log = instance.manipulation_log_update(log1_test, log2_test)
    print(updated_log)

    array_log = instance.get_log_arr(updated_log)
    print(array_log)


    list1 = [[0, 3], [4, 6], [6, 9], [9, 11], [11, 15], [15, 20]]
    result = helper.merge_adjacent_tuples(list1[:1], list1[1:])
    print(result)







