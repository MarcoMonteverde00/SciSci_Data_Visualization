import pandas as pd
import re

# Load Excel
df = pd.read_excel("INFO-01_cercacineca.xlsx")

def normalize_name(fullname: str) -> str:
    if not isinstance(fullname, str):
        return fullname

    fullname = fullname.strip()

    # Fix apostrophes only if they're fake accents (end of word)
    def fix_apostrophe(word: str) -> str:
        if word.endswith("'") and len(word) > 1:
            base = word[:-1]
            last_char = base[-1]

            replacements = {
                "a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
                "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù",
            }

            if last_char in replacements:
                return base[:-1] + replacements[last_char]
        return word

    words = fullname.split()
    words = [fix_apostrophe(w) for w in words]

    # Detect surname = continuous uppercase block(s)
    surname_parts = []
    firstname_parts = []
    for w in words:
        if w.isupper():  # part of surname
            surname_parts.append(w)
        else:  # part of firstname
            firstname_parts.append(w)

    surname = " ".join(surname_parts).upper()
    firstname = " ".join(w.capitalize() for w in firstname_parts)

    return f"{surname} {firstname}".strip()

# Apply normalization and save in new column
normalized_col = df["Cognome e Nome"].apply(normalize_name)
df.insert(2, "Cognome e Nome normalized", normalized_col)
df.insert(3, "Cognome", None)
df.insert(4, "Nome", None)

# Columns to drop in the final output
drop_cols = ["cognome list", "nome list", "orcid"]

for col in drop_cols:
    if col in df.columns:
        df = df.drop(columns=[col])

# Save back to Excel
df.to_excel("researchers_normalized.xlsx", index=False)