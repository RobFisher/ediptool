
# IP fetching code from http://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address

import os
import urllib2
import httplib


lines = []
line_number = 0
something_changed = False


def update_line(current_line, required_line):
    global lines
    global line_number
    global something_changed
    print current_line
    if current_line.strip() == required_line.strip():
        print 'Already ok.'
    else:
        print 'Changing to:'
        print required_line
        lines[line_number] = required_line
        something_changed = True


print 'Elite Dangerous IP address tool; version 1.01'


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
        file_name = drive + path
        break
    except IOError:
        pass

backup_file_name = file_name + '.backup'
backup_ok = False

if f:
    lines = f.readlines()
    f.close()
    if os.path.isfile(backup_file_name):
        print 'Backup file already exists: ' + backup_file_name
        backup_ok = True
    else:
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
    print 'Unable to find AppConfig.xml'

if backup_ok:
    port = 5100
    port_line = '   Port="' + str(port) + '"\n'
    upnp_line = '   UpnpEnabled="0"\n'
    ip_line = '    <Self name="my computer" ip="' + ip + '" port="' + str(port) + '" />\n'
    found_ip_line = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('Port="'):
            update_line(stripped_line, port_line)
        elif stripped_line.startswith('UpnpEnabled="'):
            update_line(stripped_line, upnp_line)
        elif stripped_line.startswith('<Self name="'):
            update_line(stripped_line, ip_line)
            found_ip_line = True
        elif stripped_line == '</Network>' and not found_ip_line:
            print 'Adding line:'
            print ip_line
            lines.insert(line_number, ip_line)
            line_number += 1
            found_ip_line = True
            something_changed = True
        line_number += 1

    if something_changed:
        try:
            f = open(file_name, 'w')
        except IOError:
            print 'Unable to write file.'
        else:
            print 'Updating file.'
            f.writelines(lines)
            f.close()

    f.close()

raw_input("Press Enter to continue...")
