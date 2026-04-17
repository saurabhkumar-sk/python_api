# # f = open("practice.txt",'a')

# # def write_file(txt):
# #     f.write(txt+"\n")

# # write_file("Hi everyone");
# # write_file("we are learning File I/O");
# # write_file("using Java");
# # write_file("I like Programming in Java");
file_name = 'practice.txt'

# with open(file_name,'r') as f:
#     data = f.read();

# print(data);

# new_data = data.replace("Java","Python")

# print(new_data)

# with open(file_name,'w') as f:
#     f.write(new_data);


# ///-------------------------
def check_for_word():
    word = "Python"
    with open(file_name) as f:
        data = f.read();
        if(data.find(word) != -1):
            print("Found")
            return "Found"
        else :
            print("Not found")    

def check_for_line():
    result = check_for_word()
    with open(file_name,"r") as f:
        if(result)
