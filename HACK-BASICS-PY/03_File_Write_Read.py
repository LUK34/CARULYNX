with open('data.txt','w') as file:
    file.write("Hello There\n")
    file.write("I am learning python.")

with open('data.txt','r') as file:
    print("the content of the file read are as follows: ")
    print("-------------------------------")
    data=file.read()
    print(data)
    print("-------------------------------")