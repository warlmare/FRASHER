

### ssdeep

#### Installation under Ubuntu

Install required packages.
```
$ sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip automake autoconf libtool
```
Build and install Python module.
```
sudo BUILD_LIB=1 pip install ssdeep
```


#### Installation under Windows

Generic ssdeep won't run under Windows so use this fork instead:

(https://github.com/MacDue/ssdeep-windows-32_64)

This fork includes `fuzzy_64.dll` allowing ssdeep to run on 32 and 64 bit python. 

1. Download (and extract) / clone this repo into a folder.
2. In said folder run `python setup.py install`.

