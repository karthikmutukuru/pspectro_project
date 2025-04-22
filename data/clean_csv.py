import csv
import os
import re

# folder path
folder_path = r'C:\Users\karthik\Downloads\pspectro_project\data'

# List of input files
filenames = ['ESPD_CCT1.csv', 'ESPD_CCT2.csv', 'ESPD_CCT3.csv']

def custom_format_file(filepath):
    output_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # Skipping header

        for row in reader:
            if len(row) != 2:
                continue

            label = row[0]
            power_str = row[1]

            try:
                power = int(power_str)
            except ValueError:
                continue

            if power > 0:
                # Extracting wavelength for formatting
                match = re.match(r"(\d+)nm\(mW/m\^2\)", label)
                if match:
                    wavelength_str = match.group(1)
                    formatted_label = f"{wavelength_str}nm(mW/m^2)"
                    formatted_power = f"{power / 1000:.6f}"
                    output_lines.append(f"{formatted_label}\n{formatted_power}\n")

    # to formatted .txt file
    output_filename = f"formatted_{os.path.basename(filepath).replace('.csv', '.txt')}"
    output_path = os.path.join(folder_path, output_filename)

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.writelines(output_lines)

    print(f"Formatted output written to:\n{output_path}")

if __name__ == "__main__":
    for fname in filenames:
        full_path = os.path.join(folder_path, fname)
        if os.path.exists(full_path):
            custom_format_file(full_path)
        else:
            print(f"File not found: {full_path}")
