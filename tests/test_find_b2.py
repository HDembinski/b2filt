from b2filt import find_b2
import os


def test(tmp_path):
    fake_b2 = tmp_path / "b2"
    fake_b2.write_text("")
    os.chdir(tmp_path)
    assert find_b2() == "./b2"
    p = tmp_path / "sub"
    p.mkdir()
    os.chdir(p)
    assert find_b2() == "./../b2"
