import sys
import getopt
import urllib
#import shared
from shared import *



#statePostals=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

downloadDirectory = "data/raw/"

#input a url and download the html source to the download directory
def download(url):
    fname = url.split("/")[-1]
    print "downloading " + url
    try:
        f = open(downloadDirectory + fname)
        f.close()
        print "already downloaded"
        #maybe do a timestamp check or compare the two files to see if changed
        return
    except IOError:
        pass

        #no worries
    f = file(downloadDirectory + fname, "w")
    try:
        u = urllib.urlopen(url)
        source = u.read()
        u.close()
        f.write(source)
        f.close()
    except Exception:
        print "exception! "
        f.close();
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
                return 0;
        # process arguments
        for arg in args:
            process(arg) # process() is defined elsewhere

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2



    for state in statePostals:
        download("http://www4.uwm.edu/FLL/linguistics/dialect/staticmaps/state_" + state + ".html")




if __name__ == "__main__":
    sys.exit(main())
