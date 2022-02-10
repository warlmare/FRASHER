# FRASHER

This is a rework of FRASH (FRamework to test Algorithms of Similarity Hashing) as it was described in Breitinger et al. 
[_FRASH: A framework to test algorithms of similarity hashing_](https://www.sciencedirect.com/science/article/pii/S1742287613000522). The framework allows the targeted manipulation of files 
and the evaluation of algorithms through these. The Framework is implemented in Python 3.9. For optimal performance `Ubuntu 21.04` is recommended, however the framework itself and the algorithms `Ssdeep` and `TLSH` are useable under Windows. 


## Installation 

On Linux run `Linux_MAKEFILE` which will install the following:
- Packages 
  - `build-essential` `libffi-dev` `python3` `python3-dev` `python3-pip` `automake` `autoconf` `libtool`
- Python libraries
  - `tqdm`, `tabulate`, `ssdeep`, `six`, `simhash`, `setuptools`, `regex`, `pytz`, `python-dateutil`, `py-tlsh`, `numpy`, 
  `ntlk`, `joblib`, `click`


On Windows run `Windows_MAKEFILE` which will install the following:
 ```
 
 ```
## Using the Framework



To start FRASHER please run `python3 frasher.py`. FRASH has the following options: 
```
$ python frasher.py [-h] [-v] PATH
```
- `-h` prints usage instructions on the screen.
- `-v` is the verbose mode and prints additional information during the testruns.
- `PATH` is the path to the playbook that specifies all further information for the tests. 

The FRASHER playbooks are json files have the following syntax:

```json
{
  "algorithm": {
    "ssdeep",
    "mrsh-cf"
  },
  "tests": {
    "efficiency" : {
      "filepath" : "/testfiles/file_a"
    },
    "single_common_block": {
      "filepath1" : "/testfiles/file_a", 
      "filepath2" : "/testfiles/file_b",
      "blockfilepath" : "/testfiles/file_c"
    },
    "alignment": {
    "path" : "/testfiles/alignment"
    }
  },
  "rounds": 10
}
```
For example see the `example_playbook.json`. Tests specified under `tests:` will be executed consecutively for every algorithm specified under `algorithm`.
The results of the test `rounds` will be averaged, printed to the console and appended to the playbook. 

## Framework Structure

![](/doc/Framework_overview.png)

The Folder Structure is similar to that of the  original FRASH.

```
├───lib               
│   ├───hash_functions
│   │   ├───algorithms.py
|   |   ├───mrsh_cuckoo.exe
|   |   ├───sdhash.exe
|   |   ├───sise.exe
│   │   ├───mrsh_hbft.exe
│   │   └───Jsdhash.exe
│   ├───helpers
│   │   ├───testfiles_backup
│   │   ├───helper.py
│   │   └───file_manipulation.py
│   ├───log_analysers
│   └───testers
│       ├───base_test.py
│       ├───aligment_robustness.py
│       ├───fragment_detection.py
│       ├───random_noise_resistance.py
│       └───single_common_block.py      
└───testdata
    └───2048
```
- **hash functions** 
  - Contains the interface to all algorithms in `algorithms.py` and all the executables for the algorithms.
- **helpers**
  - Contains the auxilary methods in `helper.py` and all code needed for the bytewise manipulation of files in `file_manipulation.py`.
- **log analysers**
  - Contains all Code for result representation, and analysis. 
- **testers**
  - Contains all evaluation cases that present different challenges for the algorithms. The Superclass is `BasTest` in `base_test.py`.

### Testcases

####Efficiency 

Efficiency consists of three subtests:
- **Runtime efficiency** measures the time, which the algorithm needs to process the input. Processing in this case means that we measure the time for reading the file from the device and generating the fingerprint.

## Algorithms
Usable Algorithms are: 
- `ssdeep` (Python library)
  - Produces context triggered piecewise hashes (CTPH) in string form. Widely used for simple identification purposes (e. g. in VirusTotal). See the  [ssdeep projects website](https://ssdeep-project.github.io/ssdeep/index.html) for more information. 
- `TLSH` (Python library)
  - The _Trendmicro Locality Sensitive Hash_ produces string hashes and is the defacto standard for malware detection and has been adopted in a range of projects such as VirusTotal. For more information please refer to the [official website](http://tlsh.org/).
- `mrsh-cf` (Executable)
  - Allows for Approximate Matching via _Multi Resolution Hashing_. The Algorithm does not produce any intermediate string hash but saves known hashes in a filter. The lookup strategy involves a faster cuckoo filter instead of the bloom filter that was used in the preceeding implementation, _Mrsh-2_. FOr more information please refer to Vikas Gupta and Frank Breitingers [_How Cuckoo Filter Can Improve Existing Approximate Matching Techniques_](https://www.researchgate.net/publication/292985174_How_Cuckoo_Filter_Can_Improve_Existing_Approximate_Matching_Techniques.)
  - The Executable in this repository is a updated version of the [original algorithm](https://www.fbreitinger.de/wp-content/uploads/2015/06/mrsh_cuckoo.zip) that runs on > Ubuntu 18. 
- `MRSH-v2` (Executable)
  - beta state - documentation will follow soon.
- `sdhash` (Executable)
  - beta state - documentation will follow soon.
- `SiSe` (Executable)
  - beta state - documentation will follow soon.
- `mrsh-hbft` (Executable)
  - beta state - documentation will follow soon.
- `Jsdhash` (Executable)
  - beta state - documentation will follow soon.
- `SimHash` (Python library) 
  - beta state - documentation will follow soon.

### Installation of the Algorithms

For using all available algorithms `Ubuntu 21.04` is recommended, however if you only whish to evaluate `Ssdeep` or `TLSH`, Windows 10 is sufficient.  

#### Ssdeep
##### Installation under Ubuntu
Install required packages.
```
$ sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip automake autoconf libtool
```
Build and install Python module.
```
sudo BUILD_LIB=1 pip install ssdeep
```

##### Installation under Windows

Generic ssdeep won't run under Windows so use this fork instead:

(https://github.com/MacDue/ssdeep-windows-32_64)

This fork includes `fuzzy_64.dll` allowing ssdeep to run on 32 and 64 bit python. 

1. Download (and extract) / clone this repo into a folder.
2. In said folder run `python setup.py install`.

#### TLSH

#### mrsh-cf



### Integration of other algorithms
 new algorithms have to be anchored in `lib/hash_functions/algorithms.py` and have to inherit from the class 
`Algorithm` which specifies the operations: 
- `compare_file_against_file`
- ...

The algorithms can either be implemeted through existing Python libraries or call a precompiled executable. 
