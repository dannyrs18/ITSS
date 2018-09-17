import settings

SMUGGLER_EXCLUDE_LIST = getattr(settings, 'SMUGGLER_EXCLUDE_LIST', [])
SMUGGLER_FIXTURE_DIR = getattr(settings, 'SMUGGLER_FIXTURE_DIR', None)
SMUGGLER_FORMAT = getattr(settings, 'SMUGGLER_FORMAT', 'json')
SMUGGLER_INDENT = getattr(settings, 'SMUGGLER_INDENT', 2)