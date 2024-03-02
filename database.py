"""CSC111 Winter 2023 Course Project
===============================
This module contains a collection of Python classes and functions that will be used in
this project to represent a telemental health network.
Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""
from __future__ import annotations

import csv
import random
from typing import Optional

from python_ta.contracts import check_contracts

import data_security as cp


@check_contracts
class Patient:
    """A patient that represents patient data in a telemental health network.
    Instance Attributes:
        - first_name: The first name of the patient
        - last_name: The last name of the patient
        - state: The state the patient resides in
        - date_of_birth: The date of birth of the patient (MM/DD/YY)
        - sex: The sex of the patient
        - gender: The gender identity of the patient
        - height: The height of the patient in centimeters
        - weight: The weight of the patient in kilograms
        - language: The language that the patient speaks
        - email: The email of the patient
        - phone_number: The phone number of the patient
        - prior_medication: Any prior medication that the patient has taken
        - allergies: Any allergies that the patient has
        - username: The username that the patient created when signing up
        - diagnosis: The current diagnosis given by a doctor (may be none)
        - current: The office the patient is currently at
        - destination: The office the patient is trying to go to
        - next_office: The next office of the patient
        - encrypted_data = an encrypted list of the relevant data of the patient
        - password: The password that the patient created when signing up
        - public_key: The public_key of the patient
        - private_key: the private key of the patient
    Representation Invariants:
        - len(self.first_name) > 0
        - len(self.last_name) > 0
        - len(self.state) > 0
        - self.sex in ['Female', 'Male', 'Intersex']
        - self.gender in ['Woman', 'Man', 'Trans Woman', 'Trans Man', 'Non-Binary', 'Other']
        - self.height in list(range(1, 301))
        - self.weight in list(range(1, 301))
        - len(self.language) > 0
        - len(self.email) > 0
        - ‘@’ in self.email
        - len(self.phone_number) > 0
        - len(self.username) > 0
        - len(self.encrypted_data) > 0
        - len(self.password) > 0
    """
    first_name: str
    last_name: str
    state: str
    date_of_birth: tuple[int, int, int]
    sex: str
    gender: str
    height: float
    weight: float
    language: str
    email: str
    phone_number: int
    prior_medication: Optional[list[str]]
    allergies: Optional[list[str]]
    username: str
    diagnosis: Optional[str]
    current: Optional[Office]
    destination: Optional[Office]
    next_office: Optional[Office]
    encrypted_data: list[str]
    password: str
    public_key: Optional[tuple[int, int]]
    private_key: Optional[tuple[int, int, int]]

    def __init__(self, first_name: str, last_name: str, state: str, date_of_birth: tuple[int, int, int],
                 sex: str, gender: str, height: float, weight: float, language: str, email: str,
                 phone_number: int, prior_medication: Optional[list[str]],
                 allergies: Optional[list[str]], username: str, password: str, diagnosis: Optional[str],
                 current: Optional[Office]) -> None:
        """Initialize a new patient instance.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.state = state
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.gender = gender
        self.height = height
        self.weight = weight
        self.language = language
        self.email = email
        self.phone_number = phone_number
        self.prior_medication = prior_medication
        self.allergies = allergies
        self.username = username
        self.password = password
        self.current = current
        self.destination = None
        self.next_office = None
        self.diagnosis = diagnosis
        self.encrypted_data = encrypt_patient_data(self)

    def to_string(self) -> str:
        """Return all the relevent patient information as a string.
        """
        if self.current is not None:
            return f'{self.username},{self.password},{self.first_name},{self.last_name},{self.state},' \
                   f'{self.date_of_birth[0]},{self.date_of_birth[1]},{self.date_of_birth[2]},{self.sex},' \
                   f'{self.gender},{self.height},{self.weight},{self.language},{self.email},{self.phone_number},' \
                   f'{self.diagnosis},{self.current.professional.first_name},{self.current.professional.last_name}'

        return f'{self.username},{self.password},{self.first_name},{self.last_name},{self.state},' \
               f'{self.date_of_birth[0]},{self.date_of_birth[1]},{self.date_of_birth[2]},{self.sex},{self.gender},' \
               f'{self.height},{self.weight},{self.language},{self.email},{self.phone_number},{self.diagnosis},' \
               f'{self.current},{self.current}'

    def to_list(self) -> list:
        """Return all the relevant patient information as a list of strings to be encrypted.
        """
        return [str(item) for item in [self.username, self.first_name, self.last_name, self.state, self.date_of_birth,
                                       self.sex, self.gender, self.height, self.height, self.weight, self.language,
                                       self.email, self.phone_number, self.diagnosis]]


class Medical:
    """A doctor that represents doctor data in a telemental health network.
        Instance Attributes
            - profession: A bool indicating that, if True, the medical personnel is a psychologist, otherwise they are a
             counselor.
            - first_name: The first name of the doctor
            - last_name: The last name of the doctor
            - state: The state the doctor resides in
            - degree: The degree that the doctor holds
            - gender: The gender of the doctor
            - phone_number: The phone number of the doctor
            - email: The email of the doctor
            - current_patients: A list of the current patients that the doctor is overseeing
            - specialization: Any specialization that the doctor has
            - user: Username of the doctor
            - passw: Corresponding password of the doctor
            - public_key: The public_key of the doctor
            - private_key: the private key of the doctor
        Representation Invariants:
            - len(self.first_name) > 0
            - len(self.last_name) > 0
            - len(self.language) > 0
            - len(self.degree) > 0
            - len(self.gender) > 0
            - len(self.phone_number) > 0
            - len(self.email) > 0
            - len(specialization) > 0
            - len(user) > 0
            - len(passw) > 0
        """
    profession: bool
    first_name: str
    last_name: str
    state: str
    degree: str
    gender: str
    phone_number: int
    email: str
    current_patients: list[Patient]
    specialization: str
    user: str
    passw: str

    def __init__(self, profession: str, first_name: str, last_name: str, state: str, degree: str,
                 gender: str, email: str, specialization: str, phone_number: int, user: str, passw: str) -> None:
        """Initialize a new medical instance.
        """
        if profession == "Psychologist":
            self.profession = True
        else:
            self.profession = False
        self.first_name = first_name
        self.last_name = last_name
        self.state = state
        self.degree = degree
        self.gender = gender
        self.phone_number = phone_number
        self.email = email
        self.current_patients = []
        self.specialization = specialization
        self.user = user
        self.passw = passw


@check_contracts
class Office:
    """A node that represents an office in the network.
    Instance Attributes:
    - professional: Refers to the unique doctor (psychologist or counselor) who owns the office
    - patients: Refers to the patients that the given office supports
    - channels: A mapping containing channels for this node
        Each key in the mapping refers to the doctor's office, while the
        corresponding value refers to the channel leading into that node
    - waitlist: A list of patients that are waiting to be accepted by the office/doctor
    Representation Invariants:
    - self.professional not in channels
    - all(self in self.channels[professional].endpoints for professional in self.channels)
    - all(patient not in self.waitlist for patient in patients)
    """
    professional: Medical
    patients: list[Patient]
    channels: dict[Medical, Channel]
    waitlist: list[Patient]

    def __init__(self, professional: Medical) -> None:
        """Initialize this node with the given professional and no connections to other nodes.
        """
        self.professional = professional
        self.patients = []
        self.channels = {}
        self.waitlist = []

    def waitlist_patient(self, patient: Patient) -> None:
        """Add patient to waitlist.
        Preconditions:
            - patient not in self.waitlist
            - patient not in self.patients
        """
        self.waitlist.append(patient)

    def add_patient(self, patient: Patient) -> None:
        """Add patient as an actual patient of the office.
        Preconditions:
            - patient not in self.patients
        """
        self.patients.append(patient)
        if patient in self.waitlist:
            self.waitlist.remove(patient)
        self.professional.current_patients.append(patient)
        patient.current = self


@check_contracts
class Channel:
    """The link/'virtual hallway' connecting two offices within the network.
    Instance Attributes:
        - endpoints: The two offices linked by this channel.
        - occupant: The patient who is currently being transmitted through this channel,
        or None if the channel is not in use.
    Representaion Invariants:
        - len(endpoints) == 2
        - self.occupant is not None or self.buffer == []
    """
    endpoints: set[Office]
    occupant: Optional[Patient]
    buffer: list[Patient]

    def __init__(self, office1: Office, office2: Office) -> None:
        """Initializes an empty channel with the two given offices and adds channel to offices.
        Preconditions:
            - office1 != office2
            - office1 and office2 are not already connected by a channel
        """
        self.endpoints = {office1, office2}
        office1.channels[office2.professional] = self
        office2.channels[office1.professional] = self
        self.occupant = None
        self.buffer = []

    def other_endpoint(self, office: Office) -> Office:
        """Return the other endpoint of the channel.
        Preconditions:
            - office in self.endpoints
        """
        other_endpoint = self.endpoints - {office}
        return other_endpoint.pop()

    def add_patient(self, patient: Patient, start: Office) -> None:
        """Add the given patient to this channel and update the patient's next_office attribute.
        If the channel is empty, patient is added as occupant. If not, the patient is added to the buffer.
        Preconditions:
            - start in self.endpoints
        """
        patient.next_office = self.other_endpoint(start)
        if self.occupant is None:
            self.occupant = patient
        else:
            self.buffer.append(patient)

    def remove_patient(self) -> Patient:
        """Return the channel's current occupant. The first patient in the buffer is now the occupant.
        Otherwise, the channel's occupant is None.
        Preconditions:
            - self.occupant is not None
        """
        old_occupant = self.occupant
        if self.buffer == []:
            self.occupant = None
        else:
            self.occupant = self.buffer.pop(0)
        return old_occupant


@check_contracts
class HealthNetwork:
    """Represents a health network of offices connected to each other, where a patient can move
    from one office to another office to get the help they need.
    Instance Attributes:
        - offices: A mapping of office owner (doctor) to Office in this network
        - patients: A mapping of office occupant (patient) to Office in this network
    Representation Invariants:
        - all(doctor == offices[doctor].professional for doctor in offices)
    """
    offices: dict[Medical, Office]
    patients: dict[Patient, Office]

    def __init__(self) -> None:
        """Initialize an empty health network instance.
        """
        self.offices = {}
        self.patients = {}

    def add_office(self, professional: Medical) -> Office:
        """Add a new office to the network and return it.
        Preconditions:
            - professional not in self.offices
        """
        new_office = Office(professional)
        self.offices[professional] = new_office
        return new_office

    def add_channel(self, office1: Medical, office2: Medical) -> None:
        """Create a new channel between the given offices.
        Preconditions:
            - office1 != office2
            - office1 in self.offices
            - office2 in self.offices
        """
        Channel(self.offices[office1], self.offices[office2])

    def add_patient(self, patient: Patient, office: Office) -> bool:
        """Add patient to network. Return True if successful. Otherwise, return False.
        Preconditions:
            - patient not in self.patients
            - any(office == self.offices[doctor] for doctor in self.offices)
            - patient.current_office is None
        """
        if len(office.patients) < 10:
            office.patients.append(patient)
            office.professional.current_patients.append(patient)
            self.patients[patient] = office
            return True
        else:
            return False

    def remove_patient(self, patient: Patient) -> None:
        """Remove patient from network.
        Preconditions:
            - patient in self.patients
            - patient.current_office is not None
        """
        patient.current_office.professional.current_patients.remove(patient)
        patient.current_office.patients.remove(patient)
        self.patients.pop(patient)

    def move_patient(self, patient: Patient) -> None:
        """Move patient towards desired office.
        Preconditions:
            - patient.current_office is not None
        """
        channel = patient.current_office.channels[patient.destination.professional]

        if channel.occupant is None:
            if len(patient.destination.current_patients) < 10:
                patient.destination.patients.append(patient)
                patient.destination.professional.current_patients.append(patient)
                patient.current_office = patient.destination
                self.patients[patient] = patient.destination
            else:
                channel.occupant = patient
        else:
            channel.waitlist.append(patient)


def encrypt_patient_data(patient: Patient) -> list:
    """ Encrypt patient data and return it as a list.
    """
    encrypted_data = []
    patient_data = patient.to_list()

    patient.private_key, patient.public_key = cp.generate_keys('primes.csv')

    for data in patient_data:
        encrypted_data += [cp.file_encrypt_str(str(data), patient.public_key)]

    return encrypted_data


def decrypt_patient_data(patient: Patient) -> list:
    """Returns a list of decrypted patient data.
        """
    decrypted_data = []
    encryted = patient.encrypted_data

    for data in encryted:
        decrypted_data += [cp.file_decrypt_str(data, patient.private_key)]

    return decrypted_data


def read_network(csv_file: str) -> HealthNetwork:
    """ Reads a csv_file and turns its content into a network, returning it by the end.
    """
    network = HealthNetwork()
    offices = []

    with open('passwords.csv') as passw:
        passwords = list(csv.reader(passw))

    with open(csv_file) as file:
        reader = list(csv.DictReader(file))
        reader.pop()

        for row in reader:
            email = str.lower(row['First Name']) + '.' + str.lower(row['Last Name']) + '@gmail.com'
            password = random.choice(passwords)
            user = str.lower(row['First Name']) + '.' + str.lower(row['Last Name'])
            medical = Medical(profession=row['Classification'], first_name=row['First Name'],
                              last_name=row['Last Name'], state=row['Mailing Address State'], degree=row['Credential'],
                              gender=row['Gender'], email=email, phone_number=row['Business Address Phone'], user=user,
                              passw=password, specialization=row['Specializations'])
            office = network.add_office(medical)

            # all connected implementation:
            for office2 in offices:
                Channel(office, office2)
            offices += [office]

    return network


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'random', 'data_security'],
        'disable': ['too-many-instance-attributes', 'too-many-arguments', 'too-many-locals', 'forbidden-IO-function'],
    })
