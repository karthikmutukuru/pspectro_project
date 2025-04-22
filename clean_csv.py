import csv
import os
import re

# Folder path
folder_path = r'C:\Users\karthik\Downloads\pspectro_project\data'

# List of input files
filenames = ['ESPD_CCT1.csv', 'ESPD_CCT2.csv', 'ESPD_CCT3.csv']

def custom_format_file(filepath):
    output_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header

        for row in reader:
            if len(row) != 2:
                continue

            label = row[0]
            power_str = row[1]

            try:
                power = float(power_str)
            except ValueError:
                continue

            if power > 0:
                match = re.match(r"(\d+)nm\(mW/m\^2\)", label)
                if match:
                    wavelength = match.group(1)
                    formatted_label = f"{wavelength}nm(mW/m^2)"
                    formatted_power = f"{power / 1000:.6f}"  # convert µW to mW
                    output_lines.append([formatted_label, formatted_power])

    #cleaned CSV
    output_filename = f"cleaned_{os.path.basename(filepath)}"
    output_path = os.path.join(folder_path, output_filename)

    with open(output_path, "w", newline='', encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["wavelength", "power"])  # Optional: header
        writer.writerows(output_lines)

    print(f"Cleaned and formatted file written to:\n{output_path}")

if __name__ == "__main__":
    for fname in filenames:
        full_path = os.path.join(folder_path, fname)
        if os.path.exists(full_path):
            custom_format_file(full_path)
        else:
            print(f"File not found: {full_path}")
