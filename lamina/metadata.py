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
__BUILD = 136

__IN_BETA = True
__BETA_BUILD = 1

if __IN_BETA:
    VERS = f'{__MAJOR}.{__MINOR}b-{__BETA_BUILD}'
else:
    VERS = f'{__MAJOR}.{__MINOR}.{__PATCH}.{__BUILD}'



# NOTE : The following conditional ensures that VERSION is only printed on terminal
# when it is called as a main script (that is done via build script). This prevents
# print() from unncesarily being executed when being imported by sourcecode.
if __name__ == "__main__":
    print(VERS)