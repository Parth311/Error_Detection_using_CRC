# Lab Assignment - 2
 - there are 2 files in zip folder `2020201054-Lab2.zip`  : `server.py` and `client.py`.
# Execution Flow
- the first step is to execute `server.py` with the command `python3 server.py` which will then start listening on the port no. `7006`. 
- the next step is to execute the `client.py` on a new terminal window with the command `python3 client.py` and it will connect to the port no. on which the server is listening. There can be clients running on multiple terminal windows. 
- after connecting to the server, the client asks for command line input from the user by showing `Enter the text to be sent` message.  
- the client is supposed to send the text which will always be in `UPPER-CASE` with no space at the end of the input string and upon receiving, the server will print the result on its terminal window as `No error found` if the received CRC bits match. Otherwise it shows `Error detected` message. 



