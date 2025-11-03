import pandas as pd

# === Pfade anpassen ===
csv_path = "Default Dataset(2).csv"
ldt_path = "output.ldt"

# CSV einlesen (Komma + Semikolon trennen)
df = pd.read_csv(csv_path, sep='[;,]', engine='python', header=None)
# Select only first 2 columns (Angle, Candela) - additional columns are ignored
df = df.iloc[:, :2]
df.columns = ['Angle', 'Candela']

# Sortieren nach Winkel (für Sicherheit)
df = df.sort_values('Angle')

# Calculate angular spacing (if equal spacing)
angles = df['Angle'].values
if len(angles) > 1:
    # Check if spacing is equal
    spacing = float(round(angles[1] - angles[0], 1))
    equal_spacing = all(abs(round(angles[i] - angles[i-1], 1) - spacing) < 0.1 for i in range(1, len(angles)))
    dg = spacing if equal_spacing else 0.0
else:
    dg = 0.0

# EULUMDAT file structure (complete format)
lines = []

# Line 1: Company identification
lines.append("Company/Manufacturer")

# Line 2: Type indicator (1 = point source with symmetry)
lines.append("1")

# Line 3: Symmetry indicator (0 = no symmetry, 1 = symmetry about vertical axis)
lines.append("1")

# Line 4: Number of C-planes (Mc) - for rotational symmetry, typically 1
lines.append("1")

# Line 5: Distance between C-planes (Dc) - 0.0 for single C-plane
lines.append("0.0")

# Line 6: Number of luminous intensities per C-plane (Ng)
lines.append(str(len(df)))

# Line 7: Distance between luminous intensities per C-plane (Dg)
lines.append(f"{dg:.1f}")

# Line 8: Measurement report number
lines.append("Measurement report")

# Line 9: Luminaire name
lines.append("Generic luminaire")

# Line 10: Luminaire number
lines.append("LUM001")

# Line 11: File name
lines.append("output")

# Line 12: Date/User
lines.append("2024")

# Line 13-15: Length, width, height of luminaire (mm)
lines.append("100")  # Length
lines.append("100")  # Width
lines.append("50")   # Height

# Line 16-17: Length, width of luminous area (mm)
lines.append("80")   # Length
lines.append("80")   # Width

# Line 18-21: Height of luminous area C0, C90, C180, C270 (mm)
lines.append("0")    # C0
lines.append("0")    # C90
lines.append("0")    # C180
lines.append("0")    # C270

# Line 22: Downward flux fraction (%)
lines.append("50.0")

# Line 23: Light output ratio luminaire (%)
lines.append("100.0")

# Line 24: Conversion factor for luminous intensities
lines.append("1.0")

# Line 25: Tilt of luminaire during measurement (degrees)
lines.append("0.0")

# Line 26: Number of standard sets of lamps
lines.append("1")

# Lines 27-32: Lamp data (for each set)
lines.append("1")       # Number of lamps
lines.append("LED")     # Type of lamps
lines.append("1000")    # Total luminous flux (lm)
lines.append("4000")    # Color temperature (K)
lines.append("80")      # Color rendering index
lines.append("10.0")    # Wattage including ballast

# Lines 33-42: Direct ratios for room indices k = 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0
for _ in range(10):
    lines.append("0.5")

# Line 43: Angles C (C-planes)
lines.append("0.0")

# Line 44: Angles G (Gamma angles)
gamma_angles_str = " ".join([f"{a:.1f}" for a in df["Angle"]])
lines.append(gamma_angles_str)

# Line 45+: Luminous intensity distribution (candela values for each C-plane)
cd_values_str = " ".join([str(round(c, 2)) for c in df["Candela"]])
lines.append(cd_values_str)

# Datei schreiben
with open(ldt_path, "w") as f:
    for line in lines:
        f.write(line + "\n")

print(f"EULUMDAT-Datei '{ldt_path}' erfolgreich erstellt.")
