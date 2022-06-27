from asciidoc import set_compat_mode
import pytest


@pytest.mark.parametrize(
    'inp',
    (0, 3)
)
def test_invalid_compat_mode(inp) -> None:
    with pytest.raises(ValueError):
        set_compat_mode(inp)
