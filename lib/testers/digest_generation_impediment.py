from base_test import BaseTest
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

dirname = os.path.dirname(__file__)

class DigestGenerationImpediment(BaseTest):

    def create_testdata(self, *args):

