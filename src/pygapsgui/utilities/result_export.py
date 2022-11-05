import os

import pandas

from pygapsgui.widgets.UtilityDialogs import error_dialog
from pygapsgui.widgets.UtilityDialogs import save_file_dialog


def serialize(obj: dict, how: str = "H", parent=None):

    # TODO get last directory here too
    filename = save_file_dialog(
        parent, "Export results", '.', filter=";;".join([
            'CSV (*.csv)',
            'JSON (*.json)',
        ])
    )

    if filename and filename != '':
        _, ext = os.path.splitext(filename)
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
                raise Exception("Unknown file save format.")

        except Exception as e:
            error_dialog(str(e))

    return False
