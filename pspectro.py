import numpy as np
from utils import load_spectrum, load_cmf, load_vlambda, calculate_lux, calculate_xyz


def main():
    filenames = [
        "cleaned_ESPD_CCT1.csv",
        "cleaned_ESPD_CCT2.csv",
        "cleaned_ESPD_CCT3.csv"
    ]

    cmf = load_cmf("data/cie1931_2deg_xyz.csv")
    v_lambda = load_vlambda("data/v_lambda.csv")

    for file in filenames:
        spectrum = load_spectrum(f"data/{file}", scale_factor=1e-3)

        if spectrum is None:
            continue

        print(f"\nProcessing {file}...")
        print("Cleaned Spectrum Data:\n")
        formatted_rows = []
        for index, row in spectrum.head(5).iterrows():
            wavelength_str = f"{int(row['wavelength'])}nm(mW/m^2)"
            power_str = f"{row['power']:.6f}".replace('.', ',')
            formatted_rows.append([wavelength_str, power_str])

        # Created a formatted DataFrame
        import pandas as pd
        display_df = pd.DataFrame(formatted_rows, columns=["wavelength", "power"])
        print(display_df.to_string())
         

        lux = calculate_lux(spectrum, v_lambda)
        XYZ, (x, y, z) = calculate_xyz(spectrum, cmf)
        X, Y, Z = XYZ

        xyz2deg = [np.float64(x), np.float64(y), np.float64(1 - (x + y))]
        XYZ2DEG = [np.float64(X), np.float64(Y), np.float64(Z)]

        print(f"\nLux(lx): {lux:.3f}")
        print(f"x: {x:.6f}\ny: {y:.6f}\nz: {z:.6f}")
        print(f"X: {X:.3f}\nY: {Y:.3f}\nZ: {Z:.3f}")
        print(f"\nXYZ2DEG: {XYZ2DEG}")
        print(f"xyz2deg: {xyz2deg}")
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


if __name__ == "__main__":
    main()