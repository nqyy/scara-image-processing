import serial

ser = serial.Serial('COM3', 115200)

with open("vector.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]

print(content)

for item in content:
    if(item == "up"):
        ser.write(b'u')

    elif (item == 'down'):
        ser.write('d')
    else:
        angle = item.split(": ")[-1]
        if(item[0] == 'f'):
            angle = 'a' + angle
        if(item[0] == 's'):
            angle = 'b' + angle

        for i in range (len(angle)):
            ser.write(angle[i])
        ser.write("x")

# 1000 for testing purpose
readdata = ser.read(1000)
print(readdata.decode('utf-8'))