"""
        Configuration Management for MICE
"""
import os
import pathlib as pt

import toml as tml

# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# ------------------------------------------------------ Variables ------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#

# Setting up the debug strings #
_filename = pt.Path(__file__).name.replace(".py", "")
_dbg_string = "%s:" % (_filename)

__configuration_path = os.path.join(pt.Path(__file__).parents[0], "bin", "mice_config.ini")


# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# -------------------------------------------------------FUNCTIONS ------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#

# USER CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------#
def read_config(configuration_path: str) -> dict:
    """
    Grabbing the configuration system from the configuration file path.
    :return: The configuration dictionary
    """
    ### reading the TOML string ###
    config_dict = tml.load(configuration_path)
    return config_dict




# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# -------------------------------------------------------  MAIN  --------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
if __name__ == '__main__':
    CONFIG = read_config(__configuration_path)
    print(CONFIG)
