import os
from game import AoCE
import re

MAXLEN = 512
# checksum, len 

# Match case pour interpréter les actions 
class Packet():
    id = None
    io = None
    playerID = None
    data = None


#     rx_dict = {
#     'id': re.compile(r'ID=(?P<id>\d)'),
#     'io': re.compile(r'IO=(?P<io>)'),
    
# }
    def format(self):
        output="ID:"+str(self.id)


    # def _parse_line(self, line):
    #     for key, rx in self.rx_dict.items():
    #         match = rx.search(line)
    #         if match:
    #             return key, match
    #     # if there are no matches
    #     return None, None





    def send(self, data):
        os.write(AoCE.ecriture_fd, data)
        return 1

    # def read(self):
    #     return os.read(AoCE.lecture_fd,MAXLEN)
    #     received = os.read(AoCE.lecture_fd,len)

    def read(self,len):
        splitted = received.split('\n')
        id = splitted[0]
        io = splitted[1]
        playerID = splitted[2]
        data = splitted[3]

        id = id[2:]
        io = io[2:]
        playerID = playerID[3:]

        return [id,io,playerID,data]

    def write(self, id, io, playerID, data):
    
        output = "ID:"
        output.append(id)
        output.append('\n')
        output.append("IO:")
        output.append(io)
        output.append('\n')
        output.append("PID:")
        output.append(io)
        output.append('\n')
        output.append(data)

        return output

    def interprete(self, packet):
        match(packet):
            case x:
                pass




test=Packet()
test.id=1
test.io="PING"
test.playerID=1
test.data="Start!"


print(test.write)
    


