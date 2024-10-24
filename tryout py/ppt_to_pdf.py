from pptxtopdf import convert

input_dir = [r"D:\KARTHIKEYA\VNR\EDU\SEM 4\OS\mid-1"]

for path in input_dir:
    output_dir = path
    convert(path, output_dir)
