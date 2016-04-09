import subprocess
str= subprocess.Popen(["./vol", "/Users/alexoro/Desktop/box.stl"], stdout=subprocess.PIPE).communicate()[0]
volume=float(str.split()[7]) 
print volume
