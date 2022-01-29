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



To start FRASH2.0 please run `python3 frash.py`. FRASH has the following options: 
```
$ python frash.py [-h] [-v] PATH
```
- `-h` prints usage instructions on the screen.
- `-v` is the verbose mode and prints additional information during the testruns.
- `PATH` is the path to the playbook that specifies all further information for the tests. 

The FRASH playbooks are json files have the following syntax:

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

<img src="https://viewer.diagrams.net/?tags=%7B%7D&amp;highlight=0000ff&amp;edit=_blank&amp;layers=1&amp;nav=1&amp;title=Untitled%20Diagram.drawio#R7Vxbd9soEP41fkyO7rIfm6RpHrbbdrt7dpuXHiJhm1oWqoRje3%2F9goRugG3sSJaTbppzKiE0gu8bhpkBMrJvl5sPKUjmH3EIo5FlhJuRfTeyLNOxrBH7NcJtUTI27KJglqKQV6oLvqJ%2FIS80eOkKhTBrVSQYRwQl7cIAxzEMSKsMpClet6tNcdT%2BagJmUCr4GoBILv0bhWTOe2H5dfkDRLN5%2BWXTmxRPlqCszHuSzUGI140i%2B%2F3Ivk0xJsXVcnMLIwZeiUvx3v2Op1XDUhgTnRc%2BLR7jhy%2Bzh6fnnx%2Bn0aOzuLpaXXEynkG04h3mjSXbEoEUr%2BIQMiHGyL5ZzxGBXxMQsKdryjktm5NlRO9MejnFMbkHSxQxuh9g9AwJCgB%2FwNk1bXovt5536BmmBG4aRbw3HyBeQpJuaZXyqcuR5aple%2Fx%2BXRPllejPGyQ5pXIBrhyzSnaNH73gEKrhfF7d%2FfWQ%2FPEQpzfrKLoKv32xH69cs2M8M5LiBbzFEU7zt20j%2F6kAlNBSYLobQL8NoGe6EoCmowDQtDoAUKmPKvy8iH725olezNjFyL%2BpytIWtN7PFRtMua5dZbmyvaMVTCvZ1A8rMZYHlgzt%2BClLinteA0QznCIyX7Ze6uCDBvv16Xu3%2FXaAwIxkjRdyIb3DBqdTFCAYB9vmW8aZvj5FEUyYyZW%2BLb5haBXVUu4ZnEw8hfSe%2Ff8ddK0YwseZinQgthZDG14PnxfZIxChWUyvIzgtG1KZ%2B1u8ShFkLf4drgWTb3Vj8m3R5E9kk296Kovl9mWxrJ0Wi%2FVfiz5bRV8Sge0TxovrHxmOG0QWUndwSWEk%2ByaQGMewGCyRUFQSG1ByKIf2DSOFTt3RO%2F5gicKQfUapIW0d0nICrPKet37X7HWUeviHPQJT5RHYfWmH25N23KdgCdc4XfyvGVqa4RiCZlhn1Aylq%2Bh4kmqwieZ7ADJ4nWw7dMP32WVbwlrml%2BCkG3%2FTFax35Yc3SZioSOjP35TN9ytg4UVDwfUEFlRDoTcWlGNBNYcKwNPoOYG5USK7TE0D%2BScQLGY5V59WJEJxCWoI0sUn%2BhYirPPGteF2o9n2WIikFJiOVW6J0RekGoH9hUM6ESC1h4bUee2QipOg5wwNaV%2FuEbPh9CGP2n4VD6lb5RjrKUdvDpLsH0mUwTh8x3K8NRUhyOY5lmabyjbIFJJ0%2Bw97dG0Yk7LgWz7YTMMpC%2B42zfp32%2BbdZ5gi2k9Gd1G4QYRJvKLD1bB4QUsiva8Fsptt40YUV3QVhlJyWpr4M%2BpXBFDDxSEgnUFysKKsIA0FcBUKUJalMAIEPbcbrNIK%2FoXPGOVDnOufJziHY1Gxio7yt6xGnlsQ5AuK7I8FQQUQkqBcSatun66348N6eyjJkiXFUsYUbZjOdmH7vbHbQsVV%2BN62qxjebk%2FDu%2Fx%2BA6cq8ZpdqHHugAd37F63mXAUhta0J2e0tIogaJ%2BpDSKQZSjYZ2B1zddgxsbwr03PqH7M9thwBKXXNT1UbFuQf17TY2p4%2FW%2BMSNejRHbEnusNy55GgHEce6VTYrb8EXevN6LLeNvz2O3dD6UZjhg%2FimzqqoWYtfIm7nnVwj%2BsFj3GnRmPObyO5j%2BRFkWKXuWHdLF%2Bo4ZX9teWIEbJimofHUhVEPlWHRLPsASHxFelZQ2Vb9gbJ5O3pPKe7QsID670lux8v2aAx5cGr4ZDPUQMWEYVlxIDWhr%2B6gA4iXPU8Dip8qRv2q%2F3DaePAI2KbQs6s4tvafhyclJzJ4sZbS6RWc%2BL71FUvkQl8rvXQL0YhlWrFCfEc3t0qJokzkW9hk%2Fzq1PvG1Y31FNBF0S9reFt%2FerUi6mz00f93tTe2anX2BDef06nWu%2FKV6dsYcHLP2nBS1ehdFaoinrNBao9W6aG0tCxuEAqhg%2BnJpQc%2F7wJJVsVnQib7DO0RBFIWdRGCQxw2lpH72gz8aiDkEYgxfUVRxhMhVL0tpfJ7vpIjXQExMt%2FesJvMjh%2BGlnwl%2BF3k%2F%2FrBz%2FlEZrz4ndEujhIcZY9gfQwiDXieVIHpTToRphlK6nVYx3t96SSvGpaRW6tJKWMsxjgdbcb7Li1tqcIB4s%2F5yjevy8lbDhwujPsUBOiKaRJfFGndSdEUZAnJpZ7nhCd4xbe3iKVY3EJ4MQEizU5IKhvKjUyZcEqfa5M2RFxVzugau00u3h%2BxaEq7ujU53fHFtID%2FFKMwbZRLWEVst0NrnKpQoN3tktcpHVa9elF0YJulU2eavnGU%2BouryIirxpeztlf8SSdq9gLrDxJ15vj4mhsnDstVK7DY61gWbEdswqg%2Bctl9GweiJx17YLGZorSrzsYJRfEDmVppN0Sp%2BZxHFtQ0Ek%2Flkb8jsdXunu1HCVIryNIlGyF6ljlWW2Fq7OOQkdduUEep2SOZzgG0fu6VLAWdZ3fMDtrleP6AxKy5dvuwYpgEfVGJpa7D800rNF2MGqTdZp3qLPlytK1Ejso1x7%2BL%2BPPkviD9PpyT9x1%2Bnc2nLEiSaD8Oxv9Hbw5Lno96nSFrjoP5gwLdLinBju2eUBQz8GO2%2F2G0epgTHuNwHcPODrduVpdGkNX1xhaQ%2BqjLXo64hqV%2FtLXaS5TZ%2FqoEXy%2FutSjxI4qUFIoh%2Bj3aphuelv%2FObCClPqPqtnv%2FwM%3D"/>


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
- `Ssdeep` (Python library)
  - Produces context triggered piecewise hashes (CTPH) in string form. Widely used for simple identification purposes (e. g. in VirusTotal). See the  [ssdeep projects website](https://ssdeep-project.github.io/ssdeep/index.html) for more information. 
- `TLSH` (Python library)
  - The _Trendmicro Locality Sensitive Hash_ produces string hashes and is the defacto standard for malware detection and has been adopted in a range of projects such as VirusTotal. For more information please refer to the [official website](http://tlsh.org/).
- `Mrsh-CF` (Executable)
  - Allows for Approximate Matching via _Multi Resolution Hashing_. The Algorithm does not produce any intermediate string hash but saves known hashes in a filter. The lookup strategy involves a faster cuckoo filter instead of the bloom filter that was used in the preceeding implementation, _Mrsh-2_. FOr more information please refer to Vikas Gupta and Frank Breitingers [_How Cuckoo Filter Can Improve Existing Approximate Matching Techniques_](https://www.researchgate.net/publication/292985174_How_Cuckoo_Filter_Can_Improve_Existing_Approximate_Matching_Techniques.)
  - The Executable in this repository is a updated version of the [original algorithm](https://www.fbreitinger.de/wp-content/uploads/2015/06/mrsh_cuckoo.zip) that runs on > Ubuntu 18. 
- `Sdhash` (Executable)
  - beta state - documentation will follow soon.
- `SiSe` (Executable)
  - beta state - documentation will follow soon.
- `Mrsh-HBFT` (Executable)
  - beta state - documentation will follow soon.
- `Jsdhash` (Executable)
  - beta state - documentation will follow soon.
- `Simhash` (Python library) 
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

#### Mrsh-Cf



### Integration of other algorithms
 new algorithms have to be anchored in `lib/hash_functions/algorithms.py` and have to inherit from the class 
`Algorithm` which specifies the operations: 
- `compare_file_against_file`
- ...

The algorithms can either be implemeted through existing Python libraries or call a precompiled executable. 
