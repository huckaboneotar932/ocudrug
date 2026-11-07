from ocudrug_graphrag.casework.types import MECHANISMS, SUBTYPES
from ocudrug_graphrag.workup.compat import compat, compat_matrix, explicit_entry_count


def test_matrix_shape() -> None:
    assert compat_matrix().shape == (len(MECHANISMS), len(SUBTYPES))
    assert len(MECHANISMS) == 21
    assert len(SUBTYPES) == 3


def test_explicit_entry_count() -> None:
    assert explicit_entry_count() == 47


def test_load_bearing_entries() -> None:
    assert compat("ICI-PD1-only", "UM") == 0.2
    assert compat("bispecific-TCR+HLA-A*02:01", "UM") == 1.0
    assert compat("GD2-CAR-T", "RB") == 1.0
    assert compat("CD20-targeted", "OAL") == 1.0


def test_default_is_neutral() -> None:
    assert compat("HDAC-inhibition", "UM") == 1.0


def test_all_values_in_unit_interval() -> None:
    matrix = compat_matrix()
    assert float(matrix.min()) >= 0.0
    assert float(matrix.max()) <= 1.0
