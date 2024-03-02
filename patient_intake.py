"""CSC111 Winter 2023 Course Project
===============================
This Python module contains the implementation of the application form.
Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""
from __future__ import annotations
import csv
from typing import Optional
import random
from python_ta.contracts import check_contracts
from database import Medical


@check_contracts
class ApplicationTree:
    """A decision tree that narrows down the possible doctors for a given patient
    based on the results of their application.
    Instance Attributes:
        - choice: The preference made by the patient in the application or '*' if this tree represents the start of the
        tree
        - typec: The type of the preference (Classification, State or Specialization)
        - subtrees: The subtrees of this tree which represent a possible preference made by a patient
        - doctors: A list of doctors based on the current and prior choices
        - parent: The parent tree of this tree or None if the tree represents the start of the tree
    Representation Invariants:
        - len(self.choice) > 0
        - self.typec is None or self.typec in {'Classification', 'Specialization', 'State'}
    """
    choice: str
    typec: Optional[str]
    subtrees: dict[str, ApplicationTree]
    doctors: list[Medical]
    parent: Optional[ApplicationTree]

    def __init__(self, typec: str = None, parent: ApplicationTree = None, csv_file: str = None,
                 choice: str = '*') -> None:
        """Initialize a new ApplicationTree.

        Pre-conditions:
        - self.choice =! '*' or csv_file is not None.
        - self.choice == '*' or parent is not None
        """
        self.choice = choice
        self.subtrees = {}
        if self.choice == '*':
            self.doctors = create_doctors(csv_file)
            self.parent = None
            self.typec = None
        else:
            self.parent = parent
            self.typec = typec
            self.doctors = filter_doctors(parent, self)

    def insert_possible_choice(self, choices: list[list[str]]) -> None:
        """Insert possible choices.
        Each item in choices should look like [type of choice, choice].
        Preconditions:
            - len(choices) > 0
            - all(len(list) == 2 for list in choices)
            - all(list[0] in {'Classification', 'Specialization', 'State'} for list in choices)
        """
        choices_copy = choices.copy()
        choices_copy.reverse()
        self.insert_choices_sequence(choices_copy)

    def insert_choices_sequence(self, choices: list[list[str]]) -> None:
        """Insert recursively.
        """
        if choices:
            curr = choices.pop()

            if curr[1] in self.subtrees:
                self.subtrees[curr[1]].insert_choices_sequence(choices)
            else:
                self.add_subtree(ApplicationTree(parent=self, choice=curr[1], typec=curr[0]))
                self.subtrees[curr[1]].insert_choices_sequence(choices)

    def add_subtree(self, tree: ApplicationTree) -> None:
        """Add a subtree to the current tree.
        Preconditions:
            - all(tree != self.subtrees[choice] for choice in self.subtrees)
        """
        self.subtrees[tree.choice] = tree


def all_states(csv_file: str) -> set[str]:
    """Return a set of all the states listed within the dataset.
    """
    states = set()

    with open(csv_file) as f:
        for row in csv.DictReader(f):
            states.add(row['Mailing Address State'])

    return states


def check_profession(medical: str) -> bool:
    """This function checks whether the medical individual is a psychologist or a counselor.
    """
    if medical == 'Psychologist':
        return True
    else:
        return False


def get_specializations(csv_file: str, profession: str) -> set[str]:
    """Returns a set of specializations based on the csv file and the profession
    """
    specs = set()

    with open(csv_file) as f:
        for row in csv.reader(f):
            if row[0] == profession:
                specs.add(row[1])

    return specs


def create_doctors(csv_file: str) -> list[Medical]:
    """Create all the medical attributes in a given csv file.
    """
    doctors = []

    with open('../Course Project/passwords.csv') as passw:
        passwords = list(csv.reader(passw))

    with open(csv_file) as file:
        reader = list(csv.DictReader(file))
        reader.pop()

        for row in reader:
            email = str.lower(row['First Name']) + '.' + str.lower(row['Last Name']) + '@gmail.com'
            password = random.choice(passwords)
            user = str.lower(row['First Name']) + '.' + str.lower(row['Last Name'])
            doctors.append(Medical(profession=row['Classification'], first_name=row['First Name'],
                                   last_name=row['Last Name'], state=row['Mailing Address State'],
                                   degree=row['Credential'], gender=row['Gender'], email=email,
                                   phone_number=row['Business Address Phone'], user=user, passw=password,
                                   specialization=row['Specializations']))

    return doctors


def filter_doctors(parent: ApplicationTree, subtree: ApplicationTree) -> list[Medical]:
    """ Filter parent list based on the current choices of the subtree.
    Preconditions:
        - any(subtree in parent.subtrees[choice] for choice in parent.subtrees)
    """
    current_list = parent.doctors
    filtered_list = []

    for doctor in current_list:
        if 'State' == subtree.typec:
            if doctor.state == subtree.choice:
                filtered_list.append(doctor)
        if 'Specialization' == subtree.typec:
            if subtree.choice == doctor.specialization:
                filtered_list.append(doctor)
        if 'Classification' == subtree.typec:
            if doctor.profession == check_profession(subtree.choice):
                filtered_list.append(doctor)

    return filtered_list


def list_filtered_doctors(csv_file: str, preferences: list[list[str]]) -> list:
    """Returns a list of possible doctors based on patient's preferences.
    each item in preferences should look like [type of choice, choice]

    Preconditions:
        - len(preferences) > 0
        - all(len(list) == 2 for list in preferences)
        - all(list[0] in {'Classification', 'Specialization', 'State'} for list in preferences)

    >>> list_doctors = list_filtered_doctors('../Course Project/medical_dataset.csv', [['Classification', 'Psychologist'],
     ['Specialization', 'Clinical'], ['State', 'CA']])
    >>> len(list_doctors) == 5
    True
    """
    tree = ApplicationTree(csv_file=csv_file)
    tree.insert_possible_choice(preferences)
    return tree.subtrees[preferences[0][1]].subtrees[preferences[1][1]].subtrees[preferences[2][1]].doctors


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'random', 'database'],
        'disable': ['forbidden-IO-function']
    })
