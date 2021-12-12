# Python script to generate data for our system to process 

#source
powerful_dc_chars = ["superman","wonderwoman","flash","aquaman"]
useless_dc_chars = ["batman"]
all_dc_chars = powerful_dc_chars + useless_dc_chars

#writing in file
count,f = 0,open("data.txt", "a")
while (count<901):
    f.write(all_dc_chars[count%5]+"\n")
    count+=1
f.close()