import ssdeep

filepath = "./test_file3"
hash1 = ssdeep.hash_from_file(filepath)
print(ssdeep.compare(hash1, hash1))