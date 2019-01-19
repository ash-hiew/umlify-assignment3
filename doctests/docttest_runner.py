import doctest


def doc_tests():
    doctest.testfile("doctest_shelf.txt", verbose=1)
    doctest.testfile("doctest_database.txt", verbose=1)
    doctest.testfile("doctest_commandline.txt", verbose=1)


if __name__ == "__main__":
    doc_tests()
