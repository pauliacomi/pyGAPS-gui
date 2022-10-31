import json
import operator as ope
import pathlib
import platform
import re
import typing

import qtpy
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.utilities.resources import get_resource

# Def for various substitutions
OPERATORS = {"==": ope.eq, "!=": ope.ne, ">=": ope.ge, "<=": ope.le, ">": ope.gt, "<": ope.lt}

# Regex patterns
_PATTERN_COLORS = re.compile(r"\$color\{[\s\S]*?\}")
_PATTERN_RADIUS = re.compile(r"\$radius\{[\s\S]*?\}")
_PATTERN_ENV_PATCH = re.compile(r"\$env_patch\{[\s\S]*?\}")

# Resource location
_RESOURCES_BASE_DIR = pathlib.Path(get_resource("icons/themed")).as_posix()


def _compare_v(v1: str, operator: str, v2: str) -> bool:
    """Comparing two versions."""
    v1_list, v2_list = (tuple(map(int, (v.split(".")))) for v in (v1, v2))
    return OPERATORS[operator](v1_list, v2_list)


COLORS_DARK = {
    "dark": "rgb(40, 44, 52)",
    "light": "#e4e7eb",
    "primary": "#F954FF",
    "primary-lighter": "#EF85FF",
    "primary-darker": "#8F29A6",
    "secondary": "#5a6496",
    "secondary-lighter": "#959EC9",
    "secondary-darker": "#4D5382",
    "neutral-dark": "rgb(33, 37, 43)",
    "neutral-grey": "rgb(75, 76, 83)",
    "neutral-light": "rgb(114, 123, 130)",
    "disabled-bg": "#697177",
    "disabled-fg": "#53575b",
}

COLORS_LIGHT = {
    "dark": "#4d5157",
    "light": "#f8f9fa",
    "primary": "#aa55ff",
    "primary-lighter": "#EF85FF",
    "primary-darker": "#8F29A6",
    "secondary": "#0081db",
    "secondary-lighter": "rgb(133, 160, 206)",
    "secondary-darker": "rgb(109, 139, 190)",
    "neutral-dark": "#777b84",
    "neutral-grey": "#c4c5c6",
    "neutral-light": "#dadce0",
    "disabled-bg": "#dadce0",
    "disabled-fg": "#babdc2",
}

COLORS = COLORS_DARK


def _replace_colors(match: re.Match) -> str:
    color_type = match.group().replace("$color{", "").replace("}", "")
    return COLORS[color_type]


def _parse_colors(stylesheet: str) -> "dict[str, str]":
    """Parse `$color{...}` placeholder in template stylesheet."""
    matches = _PATTERN_COLORS.finditer(stylesheet)
    return {match.group(): _replace_colors(match) for match in matches}


def _replace_rounded(match: re.Match) -> str:
    return match.group().replace("$radius{", "").replace("}", "")


def _replace_sharp(match: re.Match) -> str:
    return _PATTERN_RADIUS.sub("0", match.group())


def _parse_radius(stylesheet: str, border: str = "rounded") -> "dict[str, str]":
    """Parse `$radius{...}` placeholder in template stylesheet."""
    matches = _PATTERN_RADIUS.finditer(stylesheet)
    replace = _replace_rounded if border == "rounded" else _replace_sharp
    return {match.group(): replace(match) for match in matches}


def _multi_replace(target: str, replacements: "dict[str, str]") -> str:
    """Given a string and a replacement map, it returns the replaced string."""
    if len(replacements) == 0:
        return target

    replacements_sorted = sorted(replacements, key=len, reverse=True)
    replacements_escaped = [re.escape(i) for i in replacements_sorted]
    pattern = re.compile("|".join(replacements_escaped))
    return pattern.sub(lambda match: replacements[match.group()], target)


def _parse_env_patch(stylesheet: str) -> "dict[str, str]":
    """Parse `$env_patch{...}` placeholder in template stylesheet."""
    replacements: "dict[str, str]" = {}
    for match in re.finditer(_PATTERN_ENV_PATCH, stylesheet):
        match_text = match.group()
        json_text = match_text.replace("$env_patch", "")
        env_property: "dict[str, str]" = json.loads(json_text)

        patch_version = env_property.get("version")
        patch_qt = env_property.get("qt")
        patch_os = env_property.get("os")
        patch_value = env_property["value"]

        results: list[bool] = []
        # Parse version
        if patch_version is not None:
            for operator in OPERATORS:
                if operator not in patch_version:
                    continue
                version = patch_version.replace(operator, "")
                results.append(_compare_v(qtpy.QT_VERSION, operator, version))
                break
            else:
                raise SyntaxError(
                    f"invalid character in qualifier. Available qualifiers {list(OPERATORS.keys())}"
                ) from None
        # Parse qt binding
        if patch_qt is not None:
            if qtpy.API_NAME is None:
                results.append(False)
            results.append(patch_qt.lower() == qtpy.API_NAME.lower())
        # Parse os
        if patch_os is not None:
            results.append(platform.system().lower() in patch_os.lower())

        replacements[match_text] = patch_value if all(results) else ""
    return replacements


@QC.Slot()
def theme_apply(theme) -> None:
    """Apply a custom theme."""
    global COLORS
    qss = None
    if theme == 'light':
        qss = "stylesheets/light.qss"
        COLORS = COLORS_LIGHT
    elif theme == 'dark':
        qss = "stylesheets/dark.qss"
        COLORS = COLORS_DARK
    else:
        raise ValueError("Theme can only be light/dark.")

    with open(get_resource(qss)) as f:
        stylesheet = f.read()

    # Highlights
    replacements_color = _parse_colors(stylesheet)
    stylesheet = _multi_replace(stylesheet, replacements_color)
    # Radius
    replacements_radius = _parse_radius(stylesheet, "rounded")
    stylesheet = _multi_replace(stylesheet, replacements_radius)
    # Env
    replacements_env = _parse_env_patch(stylesheet)
    replacements_env["${path}"] = _RESOURCES_BASE_DIR  # TODO remove all refs here
    stylesheet = _multi_replace(stylesheet, replacements_env)
    # Set
    QW.QApplication.instance().setStyleSheet(stylesheet)

    # Matplotlib theme
    import matplotlib.pyplot as plt
    if theme == "dark":
        plt.style.use('dark_background')
    elif theme == "light":
        plt.style.use('default')
    # TODO add matplotlib theme change support


def theme_callback(theme) -> None:
    """Callback for theme_listener."""
    settings = QC.QSettings()
    theme_setting = settings.value("theme", "auto")
    if theme_setting == "auto":
        theme_apply(theme)


# Global thread for theme switching
THEME_DAEMON = None


def theme_listener(callback: typing.Callable[[str], None]) -> None:
    """Add a listener that automatically changes theme."""
    global THEME_DAEMON
    if THEME_DAEMON:
        return

    import threading
    import darkdetect

    THEME_DAEMON = threading.Thread(target=darkdetect.listener, args=(callback, ))
    THEME_DAEMON.daemon = True
    THEME_DAEMON.start()


def set_theme():
    """Start/set all theming components."""

    settings = QC.QSettings()
    theme_setting = settings.value("theme", "auto")

    if theme_setting not in ["dark", "light", "auto"]:
        return

    if theme_setting == "auto":
        import darkdetect
        theme_apply(darkdetect.theme().lower())
        theme_listener(theme_callback)
    else:
        theme_apply(theme_setting)
