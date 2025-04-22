import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def load_spectrum(filepath, scale_factor=1e-3):
    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.lower()
    except Exception:
        try:
            df = pd.read_csv(filepath, sep=';', header=None, names=['wavelength', 'power'])
        except Exception as e:
            print(f"Error loading spectrum from {filepath}: {e}")
            return None

    if 'wavelength' not in df.columns or 'power' not in df.columns:
        print(f"Missing required columns in {filepath}")
        return None

    df['wavelength'] = df['wavelength'].astype(str).str.extract(r"(\d+)").astype(float)
    df['power'] = pd.to_numeric(df['power'], errors='coerce') * scale_factor

    df = df[df['power'] > 0]
    df.dropna(subset=['power', 'wavelength'], inplace=True)

    print(f"Loaded spectrum data from {filepath}")
    return df

def load_cmf(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.lower()
        required_cols = {'wavelength', 'x', 'y', 'z'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"CMF file is missing columns: {required_cols - set(df.columns)}")
        return df
    except Exception as e:
        print(f"Error loading CMF from {filepath}: {e}")
        return None

def load_vlambda(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = ['wavelength', 'vlambda']
        df['wavelength'] = pd.to_numeric(df['wavelength'], errors='coerce')
        df['vlambda'] = pd.to_numeric(df['vlambda'], errors='coerce')
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading V(lambda) from {filepath}: {e}")
        return None

def calculate_xyz(spectrum, cmf):
    interp_cmf = interp1d(cmf['wavelength'], cmf[['x', 'y', 'z']].values, kind='linear', fill_value="extrapolate", axis=0)
    cmf_interp = interp_cmf(spectrum['wavelength'].values)

    delta_lambda = np.mean(np.diff(spectrum['wavelength'].values))
    XYZ = np.sum(cmf_interp * spectrum['power'].values[:, None], axis=0) * delta_lambda

    total = np.sum(XYZ)
    x = XYZ[0] / total if total != 0 else 0.0
    y = XYZ[1] / total if total != 0 else 0.0
    z=  XYZ[2] / total if total != 0 else 0.0

    return XYZ, (x, y, z)
def interpolate(ref_df, target_df, column):
    return np.interp(target_df['wavelength'], ref_df['wavelength'], ref_df[column])

def calculate_lux(spectrum_df, v_lambda_df):
    V = interpolate(v_lambda_df, spectrum_df, 'vlambda')
    power = spectrum_df['power'].values
    wavelengths = spectrum_df['wavelength'].values
    delta_lambda = np.mean(np.diff(wavelengths))

    Km = 683
    lux = Km * np.sum(power * V * delta_lambda)
    return lux    