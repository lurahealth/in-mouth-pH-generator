#!/usr/bin/env python3

import sys
import ph_sets
import argparse

def main(argv):

    biased_ph = []
    standard_ph = ph_sets.stand_ph

    # Assign non-neutral pH values set according to CLI
    parser = argparse.ArgumentParser(description='Generate pH values')
    parser.add_argument('bias', metavar='b', help='Set bad pH bias,      \
                                                   i.e. lunch or night')
    args = parser.parse_args()

    if args.bias == 'night':
        biased_ph = ph_sets.night_ph
        # Also assign time window for night
    elif args.bias == 'lunch':
        biased_ph = ph_sets.lunch_ph
        # Also assign time window for lunch 
    # add other bias labels as they are added to program
    else:
        print("ERROR : Bias not found within ph_sets.py, exiting...")
        exit()



if __name__ == "__main__":
    main(sys.argv[:])
