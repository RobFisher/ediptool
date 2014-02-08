
# IP fetching code from http://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address

import os
import urllib2
import httplib

print 'Elite Dangerous IP address tool; version 1.0'

server_name = 'www.trackip.net'
file_name = '/ip'
url = 'http://' + server_name + file_name

print 'Connecting to ' + url
conn = httplib.HTTPConnection(server_name)
conn.request('GET', '/ip')
resp = conn.getresponse()
print resp.status, resp.reason

if resp.status == 200:
    ip = resp.read()
    print 'Your external IP address is: ' + ip
else:
   print 'Connection Error: %s' % resp.reason
   print 'Doing nothing.'
conn.close()

path = ':\Program Files (x86)\Frontier\EDLaunch\Products\FORC-FDEV-D-1000\AppConfig.xml'
drives = ['C', 'D', 'E', 'F']
f = None
for drive in drives:
    try:
        print 'Looking for AppConfig.xml'
        print 'Trying ' + drive + path
        f = open(drive + path)
        break
    except IOError:
        pass

backup_file_name = drive + path + '.backup'
backup_ok = False

if f:
    lines = f.readlines()
    f.close()
    try:
        backup_file = open(backup_file_name)
    except IOError:
        try:
            print 'Making backup file ' + backup_file_name
            backup_file = open(backup_file_name, 'w')
            backup_file.writelines(lines)
            backup_file.close()
        except IOError:
            print 'Failed to make backup file, giving up.'
        else:
            print 'Made backup file.'
            backup_ok = True
    else:
        backup_file.close()
        print 'Backup file already exists: ' + backup_file_name
        backup_ok = True
else:
    print 'Unable to find AppConfig.xml'

if backup_ok:
    port = 5100
    port_line = 'Port="' + str(port) + '"'
    ip_line = '<Self name="my computer" ip="' + ip + '" port="' + str(port) + '" />'
    found_ip_line = False
    index = 0
    something_changed = False
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('Port="'):
            print stripped_line
            if stripped_line == port_line:
                print 'Already ok.'
            else:
                print 'Changing to:'
                print port_line
                lines[index] = '   ' + port_line + '\n'
                something_changed = True
        elif stripped_line.startswith('<Self name="'):
            found_ip_line = True
            print stripped_line
            if stripped_line == ip_line:
                print 'Already ok.'
            else:
                print 'Changing to:'
                print ip_line
                lines[index] = '    ' + ip_line + '\n'
                something_changed = True
        elif stripped_line == '</Network>' and not found_ip_line:
            print 'Adding line:'
            print ip_line
            lines.insert(index, '    ' + ip_line + '\n')
            index += 1
            found_ip_line = True
            something_changed = True
        index += 1
        
    if something_changed:
        try:
            f = open(drive + path, 'w')
        except IOError:
            print 'Unable to write file.'
        else:
            print 'Updating file.'
            f.writelines(lines)
            f.close()
        
    f.close()


raw_input("Press Enter to continue...")
