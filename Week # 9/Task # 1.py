for i in range(1,5):
    for j in range(4-i):
        print ('1 ',end=("\t "))     # outer loops are rows, inner loops are coloums
    for i in range(2*i-1):
         print ('*',end=("\t "))
    print ( )
