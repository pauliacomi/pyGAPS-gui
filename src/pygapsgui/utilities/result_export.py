import os
import traceback

import pandas
from qtpy import QtCore as QC

from pygapsgui.widgets.UtilityDialogs import error_detail_dialog
from pygapsgui.widgets.UtilityDialogs import save_file_dialog


def serialize(obj: dict, how: str = "H", parent=None):

    settings = QC.QSettings()
    filename = save_file_dialog(
        parent, "Export results", settings.value("resultExportDirectory", "."), filter=";;".join([
            'CSV (*.csv)',
            'JSON (*.json)',
        ])
    )

    if filename and filename != '':
        settings.setValue("resultExportDirectory", str(filename.parent))
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        try:
            if ext == '.csv':
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    if how == "V":
                        df = pandas.DataFrame(obj)
                        df.to_csv(f, index=None)
                        return True
                    else:
                        import csv
                        writer = csv.writer(f)

                        def recurse(obj):
                            for item in obj.items():
                                if isinstance(item[1], dict):
                                    writer.writerow((item[0], ))
                                    recurse(item[1])
                                elif isinstance(item[1], list):
                                    writer.writerow([item[0]] + item[1])
                                else:
                                    writer.writerow(item)

                        recurse(obj)
                        return True

            elif ext == '.json':
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    if how == "V":
                        df = pandas.DataFrame(obj).T
                        df.to_json(f, orient="split")
                        return True
                    else:
                        json.dump(obj, f)
                        return True
            else:
                raise ValueError("Unknown file save format. Use .csv or .json.")

        except Exception as e:
            error_detail_dialog(str(e), traceback.format_exc())

    return False
