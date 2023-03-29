# description of this app in 50 words
# ..



# standard imports
# ..

# internal imports
# ..

# local imports
# ..

# shared imports
# ..

# thirdparty imports
# ..



# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "LAMINA"
INFO = 'data collection agent'
AUTH = 'coenfuse'
SPAN = '2023-24'
VERS = ''
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__MAJOR = 0
__MINOR = 1
__PATCH = 0
__BUILD = 1

__IN_BETA = True
__BETA_BUILD = 1

if __IN_BETA:
    VERS = f'{__MAJOR}.{__MINOR}b-{__BETA_BUILD}'
else:
    VERS = f'{__MAJOR}.{__MINOR}.{__PATCH}.{__BUILD}'

# DESCRIPTION = f'{NAME} v{VERS} by {AUTH} {SPAN} is {INFO}'