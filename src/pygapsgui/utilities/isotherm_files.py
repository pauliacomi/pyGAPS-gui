ISOTHERM_FORMATS = {
    ".aif": ("AIF Isotherm", "isotherm_from_aif", "isotherm_to_aif"),
    ".json": ("pyGAPS JSON Isotherm", "isotherm_from_json", "isotherm_to_json"),
    ".csv": ("pyGAPS CSV Isotherm", "isotherm_from_csv", "isotherm_to_csv"),
    ".xlsx": ("pyGAPS Excel Isotherm", "isotherm_from_xl", "isotherm_to_xl"),
    ".xls": ("Legacy pyGAPS Excel Isotherm", "isotherm_from_xl", None),
}

OPEN_FILTER = "pyGAPS isotherms (" + " ".join(f"*{ext}" for ext in ISOTHERM_FORMATS) + ")"
SAVE_FILTER = ";;".join(
    f"{description} (*{ext})"
    for ext, (description, _, writer) in ISOTHERM_FORMATS.items()
    if writer is not None
)
