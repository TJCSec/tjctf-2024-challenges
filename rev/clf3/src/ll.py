a=open("output.txt","r").read().split("\n")
b=open("output2.txt","r").read().split("\n")
for i in range(len(a)):
	if (a[i] != b[i]):
		print(a[i], b[i], i);
	
