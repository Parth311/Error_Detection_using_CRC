import socket
import numpy as np
host="127.0.0.1"
port=7006

crc_key='1100'

encoding_map={}
A=np.array([[-3,-3,-4],[0,1,1],[4,3,4]])

def div_str(temp_str,crc_key):
    ind = len(crc_key)
    div=temp_str[:ind]
    while ind < len(temp_str):
        if div[0]=='0':
            div=div[1:] + temp_str[ind]
        else:
            x=''
            for i,j in zip(div[1:],crc_key[1:]):
                if i==j:
                    x+='0'
                else:
                    x+='1'
            
            div=x+temp_str[ind]
        ind+=1

    if div[0]=='1':
        x=''
        for i,j in zip(div[1:],crc_key[1:]):
            if i==j:
                x+='0'
            else:
                x+='1'
        
        div=x
    else:
        div=div[1:]
    return div
    


def get_encoded(enc_str):
    global crc_key
    temp_str = enc_str + '0'*(len(crc_key)-1)

    rem = div_str(temp_str,crc_key)

    return rem



for i in range(65,91):
    encoding_map[chr(i)]=i-64
encoding_map[' ']=27



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    while True:
        print("Enter the text to be sent: ")
        mystr=input()
        print()
        

        enc_str=(''.join(format(ord(x), 'b') for x in mystr))
        # print(enc_str)

        code=get_encoded(enc_str)
        # print(code)

        while len(mystr)%3!=0:
            mystr+=' '
        

        d=len(mystr)/3

        p=[]
        temp=[]
        for i in range(3):
            j=i
            while(j<len(mystr)):
                temp.append(encoding_map[mystr[j]])       #PENGUINS ARE ONE TO ONE
                j+=3
            p.append(temp)
            temp=[]



        p=np.array(p)

        T=np.dot(A,p)
        T=T.tolist()

        to_send=str(T)+';'+code
        # print(to_send)
        s.sendall(bytes(to_send,'utf-8'))
        # data=s.recv(1024)
        # print("server: ",repr(data))
