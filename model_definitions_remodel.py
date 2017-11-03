"""Provides keyword arguments for the creation of BaseDashModel objects.

Current models (all keyword arguments end with _kwargs):
* dnmr_two_spin: DNMR simulation for two uncoupled spins
* dnmr_AB: DNMR simulation for two coupled spins (AB quartet at the
slow-exchange limit)
"""

from dnmrplot import dnmrplot_2spin, dnmrplot_AB

dnmr_two_singlets_kwargs = {
    'name': 'dnmr-two-singlets',
    'id_': 'dnmr-2s',
    'model': dnmrplot_2spin,
    # list order reflects left-->right order of widgets in top toolbar
    'entry_names': ['va', 'vb', 'ka', 'wa', 'wb', 'pa'],
    # each Input widget has the following custom kwargs:
    'entry_dict': {
        'va': {'value': 165},
        'vb': {'value': 135},
        'ka': {
            'value': 1.5,
            'min': 0.01},
        'wa': {
            'value': 0.5,
            'min': 0.01},
        'wb': {
            'value': 0.5,
            'min': 0.01},
        'pa': {
            'value': 50,
            'min': 0,
            'max': 100}
    }
}

dnmr_AB_kwargs = {
    'name': 'dnmr-AB',
    'id_': 'dnmr-AB',
    'model': dnmrplot_AB,
    # list order reflects left-->right order of widgets in top toolbar
    'entry_names': ['va', 'vb', 'J', 'k', 'w'],
    # each Input widget has the following custom kwargs:
    'entry_dict': {
        'va': {'value': 165},
        'vb': {'value': 135},
        'J': {'value': 12},
        'k': {
            'value': 12,
            'min': 0.01},
        'w': {
            'value': 0.5,
            'min': 0.01}
    }
}
