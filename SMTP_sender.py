from sys import argv
import socket
import argparse
import time

#export PATH="$PATH:/koko/system/anaconda3/bin"
#source activate python310

parser=argparse.ArgumentParser(description="""This is an SMTP sender""")
parser.add_argument('email_file', type=str, help='this is the filename of the email body',action='store')
parser.add_argument('subject_line', type=str, help='this is the email\'s subject line, remeber to include " " around the subject',action='store')
parser.add_argument('destination_email_address', type=str, help='This is the destination email address, includes only gmail addresses for now',action='store')
parser.add_argument('source_username', type=str, help='This is the username of the source email the end is implied to be the current machine',action='store')
parser.add_argument('-s', type=str, dest='dest_serv', help='This is the destination SMTP server, defaults to gmails',action='store', default='gmail-smtp-in.l.google.com.')
args = parser.parse_args(argv[1:])

#creates client socket
out_sock = socket.socket()
out_sock.connect((args.dest_serv,25))

#current domain
current_domain = socket.gethostname()
#current time for Message-ID header
current_time = time.strftime("%H:%M:%S")

#4 necessary headers From, To, Message-ID, Subject
FROM = argv[4] + "@" + current_domain
MESSAGE_ID = current_time + "@" + current_domain
SUBJECT = argv[2]
TO = argv[3]

#helper function to show server responses
def server_response():
    server_response = out_sock.recv(1024)
    print("From server: ")
    print(server_response)

server_response()

out_sock.sendall(b'HELO ' + current_domain.encode() + b'\r\n')
print("To Server: ")
print(b'HELO ' + current_domain.encode() + b'\r\n')
server_response()

out_sock.sendall(b'MAIL FROM:<' + FROM.encode() + b'>\r\n')
print("To Server: ")
print(b'MAIL FROM:<' + FROM.encode() + b'>\r\n')
server_response()

out_sock.sendall(b'RCPT TO:<' + TO.encode() + b'>\r\n')
print("To Server: ")
print(b'RCPT TO:<' + TO.encode() + b'>\r\n')
server_response()

out_sock.sendall(b'DATA\r\n')
print("To Server: ")
print(b'DATA\r\n')
server_response()

out_sock.sendall(b'From: <' + FROM.encode() + b'>\r\n')
out_sock.sendall(b'Message-ID: <' + MESSAGE_ID.encode() + b'>\r\n')
out_sock.sendall(b'To: <' + TO.encode() + b'>\r\n')
out_sock.sendall(b'Subject: ' + SUBJECT.encode() + b'\r\n')

#read message data from email file
for line in open(argv[1], 'rb'):
    out_sock.sendall(line)

#indicate end of message
out_sock.sendall(b'\r\n.\r\n')
server_response()

out_sock.sendall(b'QUIT\r\n')
server_response()

out_sock.close()





