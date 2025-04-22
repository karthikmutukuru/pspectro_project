import os

# Specify the path of the file
filepath = "C:/Users/karthik/Downloads/pspectro_project/data/clean_ESPD_CCT1.csv"

# Check if the file exists and print the result
if os.path.exists(filepath):
    print(f"File exists: {filepath}")
else:
    print(f"File does not exist: {filepath}")
