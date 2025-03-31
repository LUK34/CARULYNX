names=[]

try:
    name=input("Enter your name: ")
    names.append(name)
    print(names)
except KeyboardInterrupt:
    print("\n You used CTRL +C, exiting from the programme.")