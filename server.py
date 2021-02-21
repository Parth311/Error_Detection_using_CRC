import socket
import ast
import numpy as np
import threading

host="127.0.0.1"
port=7006

crc_key='1100'

encoding_map={}
A=np.array([[-3,-3,-4],[0,1,1],[4,3,4]])
A_inv=np.linalg.inv(A)

for i in range(65,91):
    encoding_map[chr(i)]=i-64
encoding_map[' ']=27


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

def new_client(conn):
    while True:
        rec=b''
        while True:
            data=conn.recv(1024)
            rec+=data
            if len(data)<1024:
                break

        if rec:
                # print("client: ",repr(data))

            rec=rec.decode()
            mylst=rec.split(';')
            # print(mylst)


            T=np.array(ast.literal_eval(mylst[0]))
            # print(T)
            # data=input()
            # conn.sendall(bytes(data,'utf-8'))

            p=np.dot(A_inv,T).tolist()

            recv_str=''
            for i in range(len(p[0])):
                for l in p:
                    val=l[i]+64
                    if val<=90:
                        recv_str+=chr(int(val))
                    else:
                        recv_str+=' '
            
            # recv_str+='R'
            # while len(recv_str)%3!=0:
                # recv_str+=' '
            recv_str=recv_str.strip()
            print("Received Plain Text is: ",recv_str)

            enc_str=(''.join(format(ord(x), 'b') for x in recv_str))
            # print(enc_str)
            code=get_encoded(enc_str)

            # print(code)
            # print(mylst[1])
            if code == mylst[1]:
                print("No error Found")
            else:
                print("Error detected")
            print()
        else:
            continue



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen()
    while True:
        conn,addr=s.accept()
       
        print('Connected to ',addr)

        t1=threading.Thread(target=new_client,args=(conn,))

        t1.start()

                

