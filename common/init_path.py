import os
#Project dir
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(BASEDIR, "config")
CORES = os.path.join(BASEDIR, "api")
LIBS = os.path.join(BASEDIR, "util")
LOG = os.path.join(BASEDIR, "log")
REPORTS = os.path.join(BASEDIR, "report")
TESTCASES = os.path.join(BASEDIR, "testcases")
TESTDATA = os.path.join(BASEDIR, "testdata")

