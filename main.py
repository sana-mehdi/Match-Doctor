"""CSC111 Winter 2023 Course Project

===============================
This Python module contains the main runner.

Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""

import interface
from database import read_network


def main(csv_file: str) -> None:
    """
    This function runs the entire program.
    """
    network = read_network(csv_file)
    interface.main_system(network, csv_file)


if __name__ == '__main__':

    main('medical_dataset_small.csv')  # call main to run the project

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['interface', 'database'],
    # })
