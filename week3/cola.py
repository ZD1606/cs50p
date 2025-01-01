
amoutduo=50 
#print("amoutduo:",amoutduo)
while amoutduo>0:
    print("amoutduo:",amoutduo) 
    insertcoin=int(input("insertcoin:"))
    if insertcoin== 25 or insertcoin== 10 or insertcoin== 5:
        amoutduo=amoutduo-insertcoin
   
if amoutduo<=0:
    change_owed=amoutduo*(-1)
    print("Change owed ",change_owed) 