"""Functional tests running the characterisation and modelling dialogs from the main window."""

import importlib
import pathlib

import pytest

DATA_DIR = pathlib.Path(__file__).parent / "json"
N2_77K = DATA_DIR / "SiO2 N2 77.json"
MICROPOROUS_N2_77K = DATA_DIR / "Takeda 5A N2 77.json"


def open_files(window, *paths):
    window.open_iso(list(paths))
    return window.iso_controller.iso_current


@pytest.mark.parametrize(
    ("action", "result_key"),
    [
        ("action_area_bet", "BET area"),
        ("action_area_lang", "Langmuir area"),
        ("action_t_plot", None),
        ("action_dr_plot", "DR "),
        ("action_da_plot", "DA "),
        ("action_psd_meso", "Pore widths"),
        ("action_psd_micro", "Pore widths"),
        ("action_psd_kernel", "Pore widths"),
    ],
)
def test_characterisation(main_window, dialog_errors, action, result_key):
    path = MICROPOROUS_N2_77K if action in ("action_psd_micro", "action_psd_kernel", "action_dr_plot", "action_da_plot") else N2_77K
    isotherm = open_files(main_window, path)
    initial_properties = set(isotherm.properties)

    getattr(main_window.ui, action).trigger()

    assert dialog_errors == []
    new_keys = [str(key) for key in set(isotherm.properties) - initial_properties]
    assert new_keys, "no results were saved to the isotherm"
    if result_key:
        assert any(key.startswith(result_key) for key in new_keys), new_keys


def test_alpha_s_plot(main_window, dialog_errors):
    open_files(main_window, MICROPOROUS_N2_77K, N2_77K)
    main_window.iso_model.check_all()

    main_window.ui.action_alpha_s_plot.trigger()

    assert dialog_errors == []


@pytest.mark.parametrize("action", ["action_model_by", "action_model_guess"])
def test_modelling_adds_model_isotherm(main_window, dialog_errors, monkeypatch, action):
    from qtpy import QtWidgets as QW

    open_files(main_window, N2_77K)

    def fit_then_accept(dialog, *args, **kwargs):
        dialog.calc_auto_button.click()
        return QW.QDialog.Accepted

    dialog_module = "IsoModelByDialog" if action == "action_model_by" else "IsoModelGuessDialog"
    module = importlib.import_module(f"pygapsgui.views.{dialog_module}")
    monkeypatch.setattr(getattr(module, dialog_module), "exec", fit_then_accept, raising=False)

    getattr(main_window.ui, action).trigger()

    assert dialog_errors == []
    assert main_window.iso_model.rowCount() == 2


def test_isosteric(main_window, dialog_errors):
    paths = sorted(DATA_DIR.glob("BAX 1500 - butane - *.json"))
    open_files(main_window, *paths)
    main_window.iso_model.check_all()

    main_window.ui.action_isosteric.trigger()

    assert dialog_errors == []


@pytest.mark.parametrize("action", ["action_iast_binary_vle", "action_iast_binary_svp", "action_iast_multi_lvp"])
def test_iast(main_window, dialog_errors, action):
    open_files(main_window, DATA_DIR / "MOF-5(Zn) CH4 303.json", DATA_DIR / "MOF-5(Zn) C2H6 303.json")
    main_window.iso_model.check_all()

    getattr(main_window.ui, action).trigger()

    assert dialog_errors == []


@pytest.mark.parametrize("action", ["action_adsorbates", "action_materials"])
def test_explorers(main_window, dialog_errors, action):
    getattr(main_window.ui, action).trigger()

    assert dialog_errors == []


def test_analysis_needs_selection(main_window, dialog_errors):
    main_window.ui.action_iast_binary_vle.trigger()

    assert dialog_errors == ["Select two isotherms."]
