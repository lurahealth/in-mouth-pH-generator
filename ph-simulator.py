#!/usr/bin/env python3

import sys
import ph_sets
import bias_times
import argparse
from datetime import time

def generate_battery():
    # decrease battery level linearly from 3000mV to 1900mV
    # return battery level in millivolts 
    exit()

def generate_temperature():
    # randomly generate temperature +/- 2*C body temperature
    # return temperature as degrees celsius, rounded to 0.2
    exit()

def generate_cal_ph(ph_set):
    # use ph_sets file to randomly select pH value
    # return randomly selected pH value rounded to 0.25
    exit()

def generate_isfet(calibrated_ph):
    # create millivolt value based on arbitrary calibration profile
    # return isfet value in millivolts as integer 
    exit()

def format_row_segment(value):
    # take data segment (pH, isfet, etc) and pack into 4 char string
    # return value as 4 char string
    exit()

def format_row(time, cal_ph, temperature, battery, isfet):
    # Pack values into row following BLE packet formatting
    exit()

def add_row_to_file(fname, row):
    # add row to output file
    exit()

def main(argv):

    # globals to hold weighted pH value sets and
    # biased pH start / end times
    biased_ph       = []
    standard_ph     = ph_sets.stand_ph
    bias_start_time = time()
    bias_end_time   = time()

    # Assign non-neutral pH values set according to CLI
    parser = argparse.ArgumentParser(description='Generate pH values')
    parser.add_argument('bias', metavar='b', help='Set bad pH bias,      \
                                                             i.e. lunch or night')
    parser.add_argument('-o', '--output', dest="output_file", help='Output file name',       \
                                                           default=0)
    args = parser.parse_args()
    print(args.bias)
    print(args.output_file)

    # add other bias labels as they are added to program
    if args.bias == 'night':
        biased_ph       = ph_sets.night_ph
        bias_start_time = bias_times.night_start
        bias_end_time   = bias_times.night_end
        # REMEMBER: Check from start -> midnight and midnight -> end
        #           for night time, not just start -> end
    elif args.bias == 'lunch':
        biased_ph = ph_sets.lunch_ph
        bias_start_time = bias_times.night_start
        bias_end_time   = bias_times.night_end
    else:
        print("ERROR : Bias not found within ph_sets.py, exiting...")
        exit()




if __name__ == "__main__":
    main(sys.argv[:])
