from STT_File import STT_File
from STT_Microphone import STT_Microphone

input_type = input("Input audio through File (F) or Microphone (M): ")

if input_type=="F":
    file_name = input("Enter File name: ")
    STT_File(file_name)
elif input_type == "M":
    seconds = int(input("Enter Duration in Seconds: "))
    STT_Microphone(seconds)
else:
    print("Exit")
