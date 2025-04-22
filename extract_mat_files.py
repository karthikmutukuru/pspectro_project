import scipy.io
import pandas as pd
import numpy as np

# Load the .mat files
cie_data = scipy.io.loadmat("data/cie1931xyz1nm.mat")
vlambda_data = scipy.io.loadmat("data/vl1924e1nm.mat")

# Extract arrays
cie_xyz = cie_data['cie1931xyz1nm']
vlambda = vlambda_data['vl1924e1nm']

# Debugging
print("cie_xyz shape:", cie_xyz.shape)
print("vlambda shape:", vlambda.shape)

# adjust wavelength array
cie_len = cie_xyz.shape[0]
wavelengths = np.linspace(380, 780, cie_len)

# Save CMF to CSV
cie_df = pd.DataFrame({
    'wavelength': wavelengths,
    'x': cie_xyz[:, 0],
    'y': cie_xyz[:, 1],
    'z': cie_xyz[:, 2]
})
cie_df.to_csv("data/cie1931_2deg_xyz.csv", index=False)

# Save V(lambda)
vlambda_df = pd.DataFrame({
    'wavelength': wavelengths,
    'Vlambda': vlambda[:, 0]
})
vlambda_df.to_csv("data/v_lambda.csv", index=False)

print(" Saved: data/cie1931_2deg_xyz.csv and data/v_lambda.csv")
