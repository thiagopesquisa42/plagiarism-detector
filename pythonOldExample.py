#env python2.7
import sys

def my_function(X, Y): 
    print "Hello %s %s!" % (X, Y)


print(sys.argv)

my_function(sys.argv[1], sys.argv[2])
my_function('Mr', 'Dear')
my_function('Mr', 'Dear')
my_function('Mr', 'Dear')
#raise errors:
my_function('Mr', 'Dear',1243)
#my_function('Mr', 'Dear',oi)

