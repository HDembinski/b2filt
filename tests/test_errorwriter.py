import os
from b2filt.errorwriter import ErrorWriter


def test_pager(capsys):
    save = None
    if "PAGER" in os.environ:
        save = os.environ["PAGER"]
    os.environ["PAGER"] = "false"
    error = ErrorWriter()
    for i in range(49):
        error(f"{i} foo ")
    error.show()
    assert "Error" not in capsys.readouterr().out
    error(f"{i} bar")
    error.show()
    assert "Error" in capsys.readouterr().out
    if save is not None:
        os.environ["PAGER"] = save
    else:
        del os.environ["PAGER"]
