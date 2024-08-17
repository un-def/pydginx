from pydginx.bases import Singleton


def test() -> None:
    class S1(Singleton):
        pass

    class S2(Singleton):
        pass

    s_1_1 = S1()
    s_1_2 = S1()
    s_2 = S2()

    assert isinstance(s_1_1, S1)
    assert isinstance(s_1_2, S1)
    assert s_1_1 is s_1_2
    assert isinstance(s_2, S2)
    assert s_2 is not s_1_1
