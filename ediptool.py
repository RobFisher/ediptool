# Licensed with GPL v2. See the file LICENSE.

# IP fetching code from http://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address

import sys
import os
import urllib2
import httplib
import socket


lines = []
line_number = 0
something_changed = False


def update_line(current_line, required_line):
    global lines
    global line_number
    global something_changed
    print current_line.rstrip()
    if current_line.strip() == required_line.strip():
        print 'Already ok.\n'
    else:
        print 'Changing to:'
        print required_line
        lines[line_number] = required_line
        something_changed = True


print 'Elite Dangerous IP address tool; version 1.01'


server_name = 'www.trackip.net'
file_name = '/ip'
url = 'http://' + server_name + file_name

print \
"""
First I am going to attempt to find out your external IP address
by connecting to the following web site:
""" + url

conn = httplib.HTTPConnection(server_name)
conn.request('GET', '/ip')
resp = conn.getresponse()

if resp.status == 200:
    ip = resp.read()
    try:
        socket.inet_aton(ip)
    except socket.error:
        print '\nThe IP address I received was not valid. It was:'
        print ip
        print '\nThis is not a valid IP address.'
        print 'Therefore I am doing nothing. Sorry'
        print 'Press Enter to exit.'
        raw_input()
        sys.exit(0)
    print 'Your external IP address is: ' + ip + '\n'
    raw_input('Press enter to continue.')
else:
    print 'There was a connection error ' + str(resp.status)
    print 'with an error reason of ' + resp.reason
    print 'Therefore I am doing nothing. Sorry.'
    print 'Press Enter to exit.'
    raw_input()
    sys.exit(0)
conn.close()

path = ':\Program Files (x86)\Frontier\EDLaunch\Products\FORC-FDEV-D-1000\AppConfig.xml'
drives = ['C', 'D', 'E', 'F']
f = None

print \
"""
Now I am going to look for the Elite Dangerous configuration file
AppConfig.xml on various drives until I find it.
"""

for drive in drives:
    try:
        print 'Trying ' + drive
        f = open(drive + path)
        file_name = drive + path
        break
    except IOError:
        pass

backup_file_name = file_name + '.backup'
backup_ok = False

if f:
    print 'I found the config file here:'
    print file_name
    lines = f.readlines()
    f.close()
    if os.path.isfile(backup_file_name):
        print '\nA backup file already exists here:'
        print backup_file_name
        print 'So I will leave it and not make another one.'
        backup_ok = True
    else:
        try:
            print '\nMaking a backup file here:'
            print backup_file_name
            backup_file = open(backup_file_name, 'w')
            backup_file.writelines(lines)
            backup_file.close()
        except IOError:
            print '\nFailed to make backup file, giving up.'
        else:
            print '\nMade backup file ok.'
            backup_ok = True
else:
    print 'Unable to find AppConfig.xml'

instructions = \
"""
If you don't mind which port number you use, press enter
to use port 5100. Otherwise type the port number you
would like to use and press enter. This number must be
between 1025 and 65535.
"""

hint = \
"""
Enter a number between 1025 and 65535, or press enter
to use the default 5100, or press CTRL-C to abort.
"""

if backup_ok:
    print instructions
    port = 0
    while port == 0:
        user_input = raw_input().strip()
        if user_input == '':
            port = 5100
        else:
            try:
                port = int(user_input)
                if not 1024 < port < 65536:
                    print hint
                    port = 0
            except ValueError:
                print hint
    print

    port_line = '   Port="' + str(port) + '"\n'
    upnp_line = '   UpnpEnabled="0"\n'
    ip_line = '    <Self name="my computer" ip="' + ip + '" port="' + str(port) + '" />\n'
    found_ip_line = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('Port="'):
            update_line(line, port_line)
        elif stripped_line.startswith('UpnpEnabled="'):
            update_line(line, upnp_line)
        elif stripped_line.startswith('<Self name="'):
            update_line(line, ip_line)
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
            print 'Unable to open the config file for writing.'
            print 'Nothing changed. It did not work. Sorry.'
        else:
            print 'Updating file.'
            try:
                f.writelines(lines)
            except IOError:
                print 'Some problem writing the config file. Sorry.'
                print 'If you need to restore from backup, you can copy this file:'
                print backup_file_name
                print 'to this location:'
                print file_name
            f.close()
    else:
        print 'The config file is already correct. I changed nothing.'

    f.close()


# Code for finding local IP address from:
# http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
local_ip = s.getsockname()[0]


print \
"""
Don't forget you still need to configure your router to forward UDP port
%d to the local IP address
%s.
""" % (port, local_ip)

raw_input("Press Enter to continue...")
