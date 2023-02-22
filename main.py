import os
# import chimera
# from chimera import runCommand as rc # use 'rc' as shorthand for runCommand
# from chimera import replyobj # for emitting status messages
import numpy as np
import matplotlib.pyplot as plt
# from functions import *
from scriptgui import *

# Example usage of the function
selected_functions, directories = function_selector()
print('Selected functions:', selected_functions)
print('Directories:', directories)