#!/usr/bin/env python

from argparser import parser, valid_paths_in_args
from init_mode import init_mode
from verification_mode import verification_mode

def main():
    args = parser.parse_args()
    if not valid_paths_in_args(args.D, args.V, args.R): return
    if args.init_mode == True: 
        init_mode(
            monitored_dir = args.D, 
            verif_file_path = args.V, 
            report_file_path = args.R, 
            hash_function = args.H
        )
    elif args.verif_mode == True: 
        if args.H is not None: print("In verification mode hash will be ignored")
        verification_mode(
            monitored_path = args.D, 
            verif_file_path = args.V, 
            report_file_path = args.R,
        )

if __name__=="__main__":
    main()