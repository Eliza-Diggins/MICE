"""

Main executable file for MICE

"""
import argparse
import struct
import numpy as np
import logging as log
from utils import set_log
import pathlib as pt
from cnfg import read_config,__configuration_path
from colorama import Fore,Back,Style
import os
import toml
from datetime import datetime
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# ------------------------------------------------------ Variables ------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
_filename = pt.Path(__file__).name.replace(".py", "")
CONFIG = read_config(__configuration_path)  # reads the configuration file.
_dbg_string = "%s:" % (_filename)
__output_log_type = None


title_directory = "./bin/ect/title_text"
verbose = CONFIG["SYSTEM"]["debug_mode"]

fdbg_string = "[" + Fore.GREEN + Style.BRIGHT + "MICE-C" + Style.RESET_ALL + "]:"
done_string = "[" + Fore.CYAN + Style.BRIGHT + "DONE" + Style.RESET_ALL + "]"
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# ------------------------------------------------------ Functions ------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#

# MINI FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------#
def print_title():
    # Prints the project title and credits.
    with open(title_directory,"r") as f:
        string = f.read().encode("utf-8").decode("unicode_escape")

    print(string)

def vprint(string,**kwargs):
    # This is a verbose print, which allows us to shorten the use of the below each time we call.
    global verbose
    if verbose:
        print(string,**kwargs)
    else:
        pass

def go_exit():
    print("[RUNTIME EXECUTION SUSPENDED]")
    exit()

# CORE FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------#
def generate_cluster(dataset:dict,MOND=False):
    # Intro Debugging
    #------------------------------------------------------------------------------------------------------------------#
    func_dbgstring = "MICE:generate_cluster:"
    log.debug("%sGenerating a cluster with MOND=%s."%(func_dbgstring,MOND))

    #------------------------------------------------------------------------------------------------------------------#
    # Parsing Components                                                                                               #
    #------------------------------------------------------------------------------------------------------------------#
    print("%s Parsing Components..."%fdbg_string,end="")
    log.debug("%s Parsing Components..."%func_dbgstring)

    components = {} #-> A list of the components included in the system.


    position_data = {} #-> This is where we will end up storing the positional data for each component.
    velocity_data = {} #-> Here we store the velocity data.
    temperature_data = {} #-> Here we store the temperature data.

    print(done_string)
    log.debug("%sFinished parsing components. Found %s components."%(func_dbgstring,len(components)))

    #------------------------------------------------------------------------------------------------------------------#
    # Setting positions                                                                                                #
    #------------------------------------------------------------------------------------------------------------------#
    # At this stage, we pass each component to the create_position data function and then proceed to generate
    #  the positional data. Finally, we save the position data values in the position_data dictionary.
    #  THIS DOESN"T CHANGE WITH MOND

    print("\t%s Setting positions..."%fdbg_string)
    log.info("%s Setting Positions..."%func_dbgstring)

    for component in components:
        position_data[component]["Coords"],position_data[component]["radii"] = None #TODO: set positions

        #- Computing the density rho -#
        position_data[component]["rho"] = None #TODO: rho

    print("\t%s Setting positions...%s"%(fdbg_string,done_string))
    log.info("%s Setting Positions... Finished." % func_dbgstring)
    #------------------------------------------------------------------------------------------------------------------#
    # Setting Velocity Components                                                                                      #
    #------------------------------------------------------------------------------------------------------------------#

    print("\t%s Setting velocities..."%fdbg_string)
    log.info("%s Setting velocities..." % func_dbgstring)

    for component in components:
        velocity_data[component]["vels"] = None #TODO: set velocities

    print("\t%s Setting velocities...%s"%(fdbg_string,done_string))
    log.info("%s Setting velocities... DONE" % func_dbgstring)
    #------------------------------------------------------------------------------------------------------------------#
    # Setting Temperature Components                                                                                   #
    #------------------------------------------------------------------------------------------------------------------#

    print("\t%s Setting temperatures..."%fdbg_string)
    log.info("%s Setting temperatures..." % func_dbgstring)

    for component in components:
        temperature_data[component]["U"], = None #TODO: set temperature

    print("\t%s Setting temperatures...%s" % (fdbg_string, done_string))
    log.info("%s Setting temperatures... DONE" % func_dbgstring)
    #------------------------------------------------------------------------------------------------------------------#
    #  Data Recombination                                                                                              #
    #------------------------------------------------------------------------------------------------------------------#
    # Core objective here is to recombine all of our data into single arrays.
    #
    #
    try: #- REQUIRED SETS -#
        coords = np.concatenate([position_data[comp]["coords"] for comp in position_data if position_data[comp]["coords"]])
        radii = np.concatenate([position_data[comp]["radii"] for comp in position_data if position_data[comp]["radii"]])
    except ValueError as msg:
        print("\t%s [%s] Recombination Processing failed! Check log file for details." % (
        fdbg_string, Fore.RED + Style.BRIGHT + "CRITICAL" + Style.RESET_ALL))

        log.critical("%s Failed to recombine datasets due to the following error: %s"%(func_dbgstring,repr(msg)))
        go_exit()

    #- NON_REQUIRED SETS -#
    vels = np.concatenate([velocity_data[comp]["vels"] for comp in velocity_data if velocity_data[comp]["vels"]])
    U = np.concatenate([temperature_data[comp]["U"] for comp in temperature_data if temperature_data[comp]["U"]])

    # Returning
    return [coords,radii,vels,U]
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
# -------------------------------------------------------- MAIN ---------------------------------------------------------#
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--#
if __name__ == '__main__':
    #------------------------------------------------------------------------------------------------------------------#
    # Intro Text                                                                                                       #
    #------------------------------------------------------------------------------------------------------------------#
    print_title()

    #------------------------------------------------------------------------------------------------------------------#
    #  Argument Parsing                                                                                                #
    #------------------------------------------------------------------------------------------------------------------#
    parser = argparse.ArgumentParser() #-> initializes the argument parser.

    #- Setting up the arguments -#
    parser.add_argument("input_file",type=str,help="The desired input file.")
    parser.add_argument("-M","--MOND",action="store_true",help="This flag indicates the system should use MOND.")
    parser.add_argument("-v","--verbose",action="store_true",help="Verbose mode enables higher printing detail.")
    parser.add_argument("-lo","--log_out",type=str,help="Specify the log output location.",default = CONFIG["SYSTEM"]["DIRECTORIES"]["log_directory"])
    parser.add_argument("-l","--log_level",type=int,help="The log level.",default=20)

    args = parser.parse_args()

    #- Cleaning the inputs -#

    # managing verbosity
    if args.verbose:
        verbose = True

    vprint("%s Verbose mode enabled..."%fdbg_string)

    # Managing the logging
    vprint("%s Initializing the logging system..."%fdbg_string,end="")
    set_log(_filename,file=args.log_out,level=args.log_level)
    vprint(done_string)

    # Loading the input file #
    print("%s Loading the input file: %s."%(fdbg_string,args.input_file),end="")

    try:
        user_configuration = toml.load(args.input_file)
    except FileNotFoundError:
        print("\n%s [%s] Failed to locate the file at %s."%(fdbg_string,Fore.RED+Style.BRIGHT+"CRITICAL"+Style.RESET_ALL,args.input_file))
        go_exit()
    except toml.TomlDecodeError:
        print("\n%s [%s] File at %s was not TOML formatted." % (
        fdbg_string, Fore.RED + Style.BRIGHT + "CRITICAL" + Style.RESET_ALL, args.input_file))
        go_exit()

    print(done_string)

    #------------------------------------------------------------------------------------------------------------------#
    #                                     Performing the computations                                                  #
    #------------------------------------------------------------------------------------------------------------------#
    print("%s Generating the cluster"%fdbg_string)

    generate_cluster(user_configuration)

    print("%s Cluster Generation Complete!"%fdbg_string)





