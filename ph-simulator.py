#!/usr/bin/env python3

import sys
import ph_sets
import bias_times
import argparse
import random
import csv
import os
from datetime import date, time, datetime, timedelta

def generate_temperature():
    # randomly generate temperature +/- 2*C body temperature
    # return temperature as degrees celsius
    temp = round(random.uniform(35.0, 39.0), 1)
    return temp

def generate_isfet(calibrated_ph):
    # create millivolt value based on arbitrary calibration profile
    # return isfet value in millivolts as integer 
    offset      = 1200
    sensitivity = 50
    isfet       = offset + (calibrated_ph * sensitivity) 
    return round(isfet)

def format_row(patient_id, time, cal_ph, temperature, battery, isfet):
    # Pack values into row following BLE packet formatting
    row = "{},{},{:1.2f},{:2.1f},{},{:04d}\n".format(patient_id, time, cal_ph, temperature, battery, isfet)
    return row

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
    f_name          = os.getcwd() + "/"

    # start time for datasets
    data_start_time = datetime(2023, 3, 1, 0, 0, 0)
    data_end_time   = datetime(2023, 9, 1, 0, 0, 0)

    # Assign non-neutral pH values set according to CLI
    parser = argparse.ArgumentParser(description='Generate pH values')
    parser.add_argument('bias', metavar='b', help='Set bad pH bias,      \
                                                             i.e. lunch or night')
    parser.add_argument('patient_id', metavar='i', help='patient ID')
    parser.add_argument('-o', '--output', dest="output_file", help='Output file name',       \
                                                           default=0)
    args = parser.parse_args()

    # add other bias labels as they are added to program
    if args.bias == 'night':
        biased_ph       = ph_sets.night_ph
        bias_start_time = bias_times.night_start
        bias_end_time   = bias_times.night_end
        # REMEMBER: Check from start -> midnight and midnight -> end
        #           for night time, not just start -> end
    elif args.bias == 'lunch':
        biased_ph = ph_sets.lunch_ph
        bias_start_time = bias_times.lunch_start
        bias_end_time   = bias_times.lunch_end

    if args.output_file != 0:
        f_name = f_name + args.output_file
    else:
        f_name = f_name + "output.csv"

    # open file and write header
    f = open(f_name, 'w')
    f.write("Patient ID, Time (YYYY-MM-DD hh:mm:ss), Calibrated pH, " 
            "Temperature (*C), Battery (mV), ISFET (mV)\n")

    # generate 6 months of data
    patient_id = args.patient_id
    curr_time = data_start_time
    batt      = 3000.0
    while curr_time < data_end_time:

        # variables to go in row
        cal_ph = None
        temp   = generate_temperature()
        isfet  = None

        # check bias from start --> midnight, midnight --> end
        if args.bias == 'night':
            if (curr_time.time() >= bias_start_time and curr_time.time() <= time(23,59,0)):
                # pick biased value
                cal_ph = random.choice(biased_ph)
            elif (curr_time.time() >= time(0,0,0) and curr_time.time() <= bias_end_time):
                # pick biased value
                cal_ph = random.choice(biased_ph)
            else:
                # pick regular value
                cal_ph = random.choice(standard_ph)

        elif args.bias == 'lunch':
            if (curr_time.time() >= bias_start_time and curr_time.time() <= bias_end_time):
                # pick biased balue
                cal_ph = random.choice(biased_ph)
            else:
                # pick regular value
                cal_ph = random.choice(standard_ph)

        else:
                cal_ph = random.choice(standard_ph)

        isfet = generate_isfet(cal_ph)
        str_time = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(format_row(patient_id, str_time, cal_ph, temp, round(batt), isfet))
        #print(format_row(patient_id, str_time, cal_ph, temp, round(batt), isfet))

        # update time to next 5 mins
        curr_time = curr_time + timedelta(minutes=5)
        batt = batt - 0.025

    # close file
    f.close()
    print("Dataset generated succesfully.")

if __name__ == "__main__":
    main(sys.argv[:])
