import sys
import getopt
import urllib

from shared import *


download_directory = "data/raw/"

#input a url and download the html source to the download directory


def download(url):
    fname = url.split("/")[-1]
    print "downloading " + url
    try:
        f = open(download_directory + fname)
        f.close()
        print "already downloaded"
        #maybe do a timestamp check or compare the two files to see if changed
        return
    except IOError:
        pass

        #no worries
    f = file(download_directory + fname, "w")
    try:
        u = urllib.urlopen(url)
        source = u.read()
        u.close()
        f.write(source)
        f.close()
    except Exception:
        print "exception! "
        f.close()
    print "successfully downloaded " + url


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
       # process options
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0
        # process arguments
        for arg in args:
            process(arg)  # process() is defined elsewhere

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    for state in state_postals:
        download("http://www4.uwm.edu/FLL/linguistics/dialect/staticmaps/state_" + state + ".html")


if __name__ == "__main__":
    sys.exit(main())
