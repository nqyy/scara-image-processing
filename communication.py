import serial

ser = serial.Serial('COM3', 115200)

with open("vector/vector0.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

commands_sent_ctr = 0

ser.write(b's')
last_cmd = 's'
commands_sent_ctr = 0

reply = ser.readline().decode('utf-8')
if reply.find("OK s") == 0:
    print("OK!: Reply: ", reply)
else:
    print("Fail!: Reply: ", reply)

for item in content:
    if commands_sent_ctr >= 2000:
        ser.write(b'g')
        last_cmd = 'g'
        commands_sent_ctr = 0

        reply = ser.readline().decode('utf-8')
        if reply.find("OK " + last_cmd) == 0:
            print("OK!: Reply: ", reply)
        else:
            print("Fail!: Reply: ", reply)

    if(item == "up"):
        ser.write(b'u')
        last_cmd = 'u'
        commands_sent_ctr += 1

    elif (item == 'down'):
        ser.write(b'd')
        last_cmd = 'd'
        commands_sent_ctr += 1

    else:
        angle = item.split(": ")[-1]
        if(item[0] == 'f'):
            angle = 'a' + angle
        if(item[0] == 's'):
            angle = 'b' + angle

        for i in range(len(angle)):
            ser.write(angle[i].encode('utf-8'))

        last_cmd = angle
        commands_sent_ctr += 1

    print(last_cmd)
    reply = ser.read(ser.inWaiting()).decode('utf-8')
    print(reply)

ser.write(b'g')
last_cmd = 'g'

reply = ser.readline().decode('utf-8')
if reply.find("OK " + last_cmd) == 0:
    print("OK!: Reply: ", reply)
else:
    print("Fail!: Reply: ", reply)

while True:
    reply = ser.readline().decode('utf-8')
    print(reply)
    if reply.find("OK k") == 0:
        break
