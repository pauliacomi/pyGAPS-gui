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


@pytest.mark.parametrize(
    ("model_name", "dialog_name", "function"),
    [
        ("AreaBETModel", "AreaBETDialog", "area_BET_raw"),
        ("AreaLangModel", "AreaLangDialog", "area_langmuir_raw"),
    ],
)
def test_unexpected_calculation_errors_propagate(main_window, monkeypatch, model_name, dialog_name, function):
    module = importlib.import_module(f"pygapsgui.models.{model_name}")
    view_module = importlib.import_module(f"pygapsgui.views.{dialog_name}")
    view = getattr(view_module, dialog_name)(parent=main_window)
    model = getattr(module, model_name)(open_files(main_window, N2_77K), view)

    def broken_api(*args, **kwargs):
        raise TypeError("API mismatch")

    monkeypatch.setattr(module, function, broken_api)
    with pytest.raises(TypeError, match="API mismatch"):
        model.calculate()


@pytest.mark.parametrize(
    ("model_name", "dialog_name", "function"),
    [
        ("AreaBETModel", "AreaBETDialog", "area_BET_raw"),
        ("AreaLangModel", "AreaLangDialog", "area_langmuir_raw"),
    ],
)
def test_failed_recalculation_invalidates_results(
    main_window, monkeypatch, dialog_errors, model_name, dialog_name, function,
):
    from pygaps.utilities.exceptions import CalculationError
    from qtpy import QtWidgets as QW

    module = importlib.import_module(f"pygapsgui.models.{model_name}")
    view_module = importlib.import_module(f"pygapsgui.views.{dialog_name}")
    view = getattr(view_module, dialog_name)(parent=main_window)
    model = getattr(module, model_name)(open_files(main_window, N2_77K), view)
    assert model.has_result
    assert model.result_dict()

    def failed(*args, **kwargs):
        raise CalculationError("not enough points <3")

    monkeypatch.setattr(module, function, failed)
    model.calc_auto()

    assert not model.has_result
    save_buttons = [
        button for button in view.button_box.buttons()
        if view.button_box.buttonRole(button) == QW.QDialogButtonBox.ButtonRole.AcceptRole
    ]
    assert save_buttons and all(not button.isEnabled() for button in save_buttons)
    assert not view.export_btn.isEnabled()
    with pytest.raises(CalculationError, match="No valid"):
        model.result_dict()
    assert not model.export_results()
    original = dict(model.isotherm.properties)
    main_window.save_analysis_results(model)
    assert model.isotherm.properties == original
    assert len(dialog_errors) == 2
    assert "not enough points <3" in view.output.toPlainText()


def test_empty_results_cannot_be_saved(main_window, monkeypatch):
    import numpy as np

    from pygapsgui.models import PlotTModel as module
    from pygapsgui.views.PlotTDialog import PlotTDialog

    view = PlotTDialog(parent=main_window)
    model = module.PlotTModel(open_files(main_window, N2_77K), view)
    monkeypatch.setattr(module, "t_plot_raw", lambda *args, **kwargs: ([], np.array([])))

    model.calc_auto()

    assert not model.has_result
    assert view.res_table.rowCount() == 0
    assert "No calculation results" in view.output.toPlainText()


def test_alpha_s_reference_failure_is_reported(main_window, monkeypatch):
    from pygaps.utilities.exceptions import CalculationError

    from pygapsgui.models import PlotAlphaSModel as module
    from pygapsgui.views.PlotAlphaSDialog import PlotAlphaSDialog

    open_files(main_window, MICROPOROUS_N2_77K, N2_77K)
    target = main_window.iso_controller.iso_current
    reference = main_window.iso_model.item(0).data()

    def failed(*args, **kwargs):
        raise CalculationError("reference fit failed")

    monkeypatch.setattr(module, "area_BET", failed)
    view = PlotAlphaSDialog(parent=main_window)
    model = module.PlotAlphaSModel(target, reference, view)

    assert not model.has_result
    assert "reference fit failed" in view.output.toPlainText()
    model.calc_auto()
    assert not model.has_result
    assert "valid reference area" in view.output.toPlainText()
