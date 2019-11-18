import pytest
from django_scopes import scope

from pretalx.cfp.flow import i18n_string


@pytest.mark.parametrize('data,locales,expected', (
    ('Submission', ['en'], {'en': 'Submission'}),
    ('Submission', ['en', 'de'], {'en': 'Submission', 'de': 'Submission'}),
    ('Submission', ['en', 'de', 'xx'], {'en': 'Submission', 'de': 'Submission', 'xx': 'Submission'}),
    ({'en': 'Submission'}, ['en'], {'en': 'Submission'}),
    ({'en': 'Submission'}, ['en', 'de'], {'en': 'Submission', 'de': 'Submission'}),
    ({'en': 'Submission', 'de': 'Submission'}, ['en'], {'en': 'Submission', 'de': 'Submission'}),
    ({'en': 'Submission', 'de': 'Submission'}, ['en', 'de'], {'en': 'Submission', 'de': 'Submission'}),
    ({'en': 'Submission', 'de': 'WRONG'}, ['en', 'de'], {'en': 'Submission', 'de': 'WRONG'}),
))
def test_i18n_string(data, locales, expected):
    assert i18n_string(data, locales).data == expected


@pytest.mark.django_db
def test_cfp_flow(event):
    with scope(event=event):
        assert event.settings.cfp_flow == ''
        event.cfp_flow.save_config(event.cfp_flow.get_config(None))
        assert event.settings.cfp_flow == '{"steps": {}}'
