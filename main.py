import pandas as pd

# === Pfade anpassen ===
csv_path = "Default Dataset(2).csv"
ldt_path = "output.ldt"

# CSV einlesen (Komma + Semikolon trennen)
df = pd.read_csv(csv_path, sep='[;,]', engine='python', header=None)
# Select only the first 2 columns if there are more
df = df.iloc[:, :2]
df.columns = ['Angle', 'Candela']

# Sortieren nach Winkel (für Sicherheit)
df = df.sort_values('Angle')

# Header (minimaler generischer Aufbau)
header = [
    "Eulumdat file",
    "1",             # Number of lamps
    "1000.0",        # Luminous flux (lm)
    "1.0",           # Multiplier
    "0.0",           # Tilt (unused)
    "Generic luminaire",  # Luminaire name
    "None",          # File name
    "None",          # Date
    "cd",            # Unit type
    "1",             # Symmetry (1 = rotational)
    "1",             # # of C-planes
    str(len(df)),    # # of Gamma angles
    "0.0",           # Distance between C-planes
]

# C- and Gamma-angles
gamma_angles = " ".join([str(round(a, 1)) for a in df["Angle"]])
cd_values = " ".join([str(round(c, 2)) for c in df["Candela"]])

# Datei schreiben
with open(ldt_path, "w") as f:
    for line in header:
        f.write(line + "\n")
    f.write(gamma_angles + "\n")
    f.write(cd_values + "\n")

print(f"EULUMDAT-Datei '{ldt_path}' erfolgreich erstellt.")
