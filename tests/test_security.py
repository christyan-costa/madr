from madr.security import sanitize_string


def test_sanitize_string_function():
    st1 = 'Machado de Assis'
    st2 = 'Manuel        Bandeira'
    st3 = 'Edgar Alan Poe         '
    st4 = 'Androides Sonham Com Ovelhas Elétricas?'
    st5 = '  breve  história  do tempo'
    st6 = 'O mundo assombrado pelos demônios'

    assert sanitize_string(st1) == 'machado de assis'
    assert sanitize_string(st2) == 'manuel bandeira'
    assert sanitize_string(st3) == 'edgar alan poe'
    assert sanitize_string(st4) == 'androides sonham com ovelhas elétricas'
    assert sanitize_string(st5) == 'breve história do tempo'
    assert sanitize_string(st6) == 'o mundo assombrado pelos demônios'
