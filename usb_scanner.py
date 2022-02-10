from pyudev import Context, Monitor
import psutil
import glob
import hashlib
import time



def hash_file(filename):
   """"This function returns the SHA-1 hash of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

# virus hash database
virus_hash = ['68bb75d24bdb38da03227dc3d90452019f96c5c1']
context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem='block')

i = 0

while(1):
    for action, device in monitor:
        #print(i)
        i=(i+1)%2
        if(action == 'add' and i == 0):
            print('{0}: {1}'.format(action, device.device_node))
            partition = device.device_node
            time.sleep(1)
            for p in psutil.disk_partitions():
                #print(p.device)
                if p.device == partition:
                    print("  {}: {}".format(p.device, p.mountpoint))
                    files = glob.glob(p.mountpoint + "/*.txt")
                    print("***list of files:\n")
                    for f in files:
                        print("\t\t"+f)
                        if( hash_file(f) in virus_hash ):
                            print("\n************** x USB has VIRUS x **************")
                            break;

            
