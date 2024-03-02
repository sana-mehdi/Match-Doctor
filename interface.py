"""CSC111 Winter 2023 Course Project

===============================
This Python module contains the user interface.

Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""
from __future__ import annotations
import random
from tkinter.constants import BOTH, LEFT, N, NSEW, NW, S, TOP, X, YES
from ttkbootstrap import Window
import ttkbootstrap as ttk
from patient_intake import all_states, get_specializations, list_filtered_doctors
from database import Patient, Medical, HealthNetwork
from interface_helpers import info_row, validate_length, check_user, check_pass, form_entry, combo, \
    validate_text, validate_phone, validate_email


def main_system(network: HealthNetwork, csv_file: str) -> None:
    """
    A function that starts the entire user interface. This contains the first window that pops up.
    """

    page = Window(themename='morph')

    page.title("Welcome!")

    page.geometry('300x250')

    title = ttk.Label(page, text="Match", font='Modern 50 bold')
    title.pack()

    btn_frame = ttk.Frame(page)
    btn_frame.pack(pady=20, padx=30, fill='none')
    ttk.Button(btn_frame, text='Sign Up', style="primary-outline",
               command=lambda: sign_up(page, network, csv_file)).pack(ipadx=10, pady=20)
    ttk.Button(btn_frame, text='Sign In', style='primary-outline',
               command=lambda: sign_in(page, network, csv_file)).pack(ipadx=10)

    page.mainloop()


def sign_in_doctor(app1: ttk.Toplevel, network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the doctor login window
    """
    # close window
    app1.withdraw()

    # create sign in page
    app = ttk.Toplevel(title='Sign In')
    app.geometry('400x400')

    # create label
    lbl_sign = ttk.Label(app, text="Sign In", font='Modern 50 bold')
    lbl_sign.pack(pady=30)

    # create frame
    sign_frame = ttk.LabelFrame(app, text='Doctor', padding=10)
    sign_frame.pack(fill=X, anchor=N, padx=30)

    # create username entry
    user_row = ttk.Frame(sign_frame)
    user_row.pack(fill=X, expand=YES)
    user_lbl = ttk.Label(user_row, text="Username", width=8)
    user_lbl.pack(side=LEFT, padx=(15, 0))
    user_var = ttk.StringVar(value="")
    user_ent = ttk.Entry(user_row, textvariable=user_var, validatecommand=validate_length, validate='focus')
    user_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # create password entry
    pass_row = ttk.Frame(sign_frame)
    pass_row.pack(fill=X, expand=YES, pady=15)
    pass_lbl = ttk.Label(pass_row, text="Password", width=8)
    pass_lbl.pack(side=LEFT, padx=(15, 0))
    pass_var = ttk.StringVar(value="")
    pass_ent = ttk.Entry(pass_row, textvariable=pass_var, validatecommand=validate_length, validate='focus')
    pass_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # create button to login
    btn_row = ttk.Frame(sign_frame)
    btn_row.pack(fill=X, expand=YES, pady=30)
    in_btn = ttk.Button(
        master=btn_row,
        text="Sign In",
        command=lambda: sign_in_btn_doctor(app, user_var, pass_var, network, csv_file),
        width=8
    )
    in_btn.pack(padx=5)


def sign_in_btn_doctor(app: ttk.Toplevel, user: ttk.StringVar, passw: ttk.StringVar,
                       network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the doctor window for doctors that sign in
    """
    doc = None
    for doctor in network.offices:
        if user.get() == doctor.user and passw.get() == doctor.passw:
            doc = doctor

    if doc is not None:
        app.withdraw()
        doc_win = ttk.Toplevel(title='Doctor')
        doc_win.geometry('1000x900')

        # create label
        lbl_sign = ttk.Label(doc_win, text="Doctor", font='Modern 30 bold')
        lbl_sign.pack(pady=30)

        screen = ttk.Frame(doc_win)
        screen.pack(fill=BOTH, anchor=NW)

        for i in range(3):
            screen.columnconfigure(i, weight=1)
        screen.rowconfigure(0, weight=1)

        col1 = ttk.Frame(screen)
        col1.grid(row=0, column=0, sticky=NSEW)

        # doc info
        doc_info = ttk.Labelframe(col1, text='Account', padding=10)
        doc_info.pack(side=TOP)

        btn_row = ttk.Frame(doc_info)
        btn_row.pack(fill=X, expand=YES, pady=30)
        in_btn = ttk.Button(
            master=doc_info,
            text='Sign Out',
            command=lambda: sign_out(doc_win, network, csv_file)
        )
        in_btn.pack(padx=5)

        # display doc info
        name_row = ttk.Frame(doc_info)
        name_row.pack(fill=X, expand=YES)
        name_lbl = ttk.Label(name_row, text=f'Name: {doc.first_name} {doc.last_name}')
        name_lbl.pack(side=TOP, padx=(15, 0))

        col3 = ttk.Frame(screen)
        col3.grid(row=0, column=2, sticky=NSEW)

        new_patient_info = ttk.Labelframe(col3, text='New Requests', padding=100)
        new_patient_info.pack()
        new_patients_row = ttk.Frame(doc_info)
        new_patients_row.pack(fill=X, expand=YES)

        for patient in network.offices[doc].waitlist:
            btn_row = ttk.Frame(new_patient_info)
            btn_row.pack(fill=X, expand=YES, pady=10)
            in_btn, decline_btn = ttk.Button(
                master=btn_row,
                text=f'{patient.first_name} {patient.last_name}',
                command=lambda: add_patient_btn(doc_win, in_btn, decline_btn, doc,
                                                patient, ttk.Frame(patient_info), network, csv_file),
                width=len(f'{patient.first_name} {patient.last_name}')
            ), ttk.Button(
                master=btn_row,
                text='Decline',
                command=lambda: decline_patient_btn(in_btn, decline_btn, patient),
                width=len('Decline')
            )

            in_btn.pack(padx=5)
            decline_btn.pack(padx=5)

        col2 = ttk.Frame(screen)
        col2.grid(row=0, column=1, sticky=NSEW)

        # current patients label
        patient_info = ttk.Labelframe(col2, text='Current Patients', padding=100)
        patient_info.pack(anchor='center')
        patients_row = ttk.Frame(doc_info)
        patients_row.pack(fill=X, expand=YES)

        for patient in doc.current_patients:
            btn_row = ttk.Frame(patient_info)
            btn_row.pack(fill=X, expand=YES, pady=10)
            in_btn = ttk.Button(
                master=btn_row,
                text=f'{patient.first_name} {patient.last_name}',
                command=lambda: patient_btn(app, patient, network, csv_file),
                width=len(f'{patient.first_name} {patient.last_name}')
            )
            in_btn.pack(padx=5)

        doc_win.mainloop()


def add_patient_btn(app: ttk.Toplevel, accept: ttk.Button, decline: ttk.Button,
                    doc: Medical, pat: Patient, frame: ttk.Frame(), network: HealthNetwork, csv_file: str) -> None:
    """Adds given patient as a button under current patients.
    """
    if len(doc.current_patients) < 10:
        accept.destroy()
        decline.destroy()
        btn_row = frame
        btn_row.pack(fill=X, expand=YES, pady=10)
        in_btn = ttk.Button(
            master=btn_row,
            text=f'{pat.first_name} {pat.last_name}',
            command=lambda: patient_btn(app, pat, network, csv_file),
            width=len(f'{pat.first_name} {pat.last_name}')
        )
        in_btn.pack(padx=5)
        doc.current_patients.append(pat)


def decline_patient_btn(accept: ttk.Button, decline: ttk.Button, pat: Patient) -> None:
    """Declining a patient. Removes option to add as patient. Changes patient current office and diagnosis to None.
    """
    accept.destroy()
    decline.destroy()
    pat.current = None
    pat.diagnosis = None


def sign_out(win: ttk.Toplevel, network: HealthNetwork, csv_file: str) -> None:
    """Signs out of application, displaying home screen again.
    """
    win.destroy()
    main_system(network, csv_file)


def patient_btn(app: ttk.Toplevel, pat: Patient, network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the respective patient information window.
    """
    # close window
    app.withdraw()

    # create sign in page
    pat_win = ttk.Toplevel(title='Patient Information')
    pat_win.geometry('1000x900')

    # create label
    lbl_sign = ttk.Label(pat_win, text='Paitient: ' + f'{pat.first_name} {pat.last_name}',
                         font='Modern 50 bold')
    lbl_sign.pack(pady=30)

    # create frame
    sign_frame = ttk.LabelFrame(app, text=f'{pat.first_name} {pat.last_name}', padding=10)
    sign_frame.pack(fill=X, anchor=N, padx=30)

    screen = ttk.Frame(pat_win)
    screen.pack(fill=BOTH, anchor=NW)

    for i in range(2):
        screen.columnconfigure(i, weight=1)
    screen.rowconfigure(0, weight=1)

    col1 = ttk.Frame(screen)
    col1.grid(row=0, column=0, sticky=NSEW)

    # doc info
    doc_info = ttk.Labelframe(col1, text='Account', padding=10)
    doc_info.pack(side=TOP)

    btn_row = ttk.Frame(doc_info)
    btn_row.pack(fill=X, expand=YES, pady=5)
    in_btn = ttk.Button(
        master=doc_info,
        text='Sign Out',
        command=lambda: sign_out(pat_win, network, csv_file)
    )
    in_btn.pack(padx=5)

    col2 = ttk.Frame(screen)
    col2.grid(row=0, column=1, sticky=NSEW)

    pat_info = ttk.Labelframe(col2, text='Patient:', padding=10)
    pat_info.pack(side=TOP)

    # Add Patient info to the Screen
    info_row(pat_info, f'Name: {pat.first_name} {pat.last_name}')
    info_row(pat_info, f'State: {pat.state}')
    info_row(pat_info, f'Date of Birth: {pat.date_of_birth[0]}/{pat.date_of_birth[1]}/{pat.date_of_birth[2]}')
    info_row(pat_info, f'Sex: {pat.sex}')
    info_row(pat_info, f'Gender: {pat.gender}')
    info_row(pat_info, f'Height: {pat.height} cm')
    info_row(pat_info, f'Weight: {pat.weight} kg')
    info_row(pat_info, f'Language: {pat.language}')
    info_row(pat_info, f'Email: {pat.email}')
    info_row(pat_info, f'Phone: {pat.phone_number}')
    info_row(pat_info, 'Medication: ' + ', '.join(pat.prior_medication))
    info_row(pat_info, 'Allergies: ' + ', '.join(pat.allergies))

    # diagnosis entry
    diagnosis_frame = ttk.LabelFrame(pat_win, text='Diagnosis:', padding=10)
    diagnosis_frame.pack(fill=X, anchor=S, padx=10)

    # create diagnosis entry
    user_row = ttk.Frame(diagnosis_frame)
    user_row.pack(fill=X, expand=YES)
    user_var = ttk.StringVar(value="")
    user_ent = ttk.Entry(user_row, textvariable=user_var, validatecommand=validate_length, validate='focus')
    user_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # create button to submit
    submit = ttk.Frame(diagnosis_frame)
    submit.pack(fill=X, expand=YES, pady=30)
    submit_btn = ttk.Button(
        master=btn_row,
        text="Submit",
        command=lambda: submit_diagnosis(pat, user_var.get()),
        width=8
    )
    submit_btn.pack(padx=5)

    pat_win.mainloop()


def submit_diagnosis(pat: Patient, diagnosis: str) -> None:
    """Submits diagnosis to patient and presents window for confirmation.
    """
    pat.diagnosis = diagnosis
    confirm_win = ttk.Toplevel(title='Sent')
    confirm_win.geometry('300x150')

    # create label
    lbl_sign = ttk.Label(confirm_win, text='Diagnosis sent!',
                         font='Modern 30 bold', anchor='center')
    lbl_sign.pack(pady=30)


def sign_up(app: ttk.Window, network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates a new window for patients to sign up with the program.
    """
    app.withdraw()

    # creating the new window
    app = ttk.Toplevel(title="Sign Up")
    app.geometry('525x475')

    # creating the title
    lbl_sign = ttk.Label(app, text="Sign Up", font='Modern 50 bold')
    lbl_sign.pack(padx=10, pady=15)

    # create frame
    sign_frame = ttk.LabelFrame(app, text='Basic Information', padding=10)
    sign_frame.pack(fill=X, anchor=N, padx=30)

    # form variables
    first_name = ttk.StringVar(value="")
    last_name = ttk.StringVar(value="")
    email = ttk.StringVar(value="")
    phone = ttk.StringVar(value="")

    # create form entries, combo boxes, and date entry
    form_entry("First Name", first_name, sign_frame, app.register(validate_text))
    form_entry("Last Name", last_name, sign_frame, app.register(validate_text))

    cont = ttk.Frame(sign_frame)
    cont.pack(fill=X, pady=5)

    lbl = ttk.Label(master=cont, text="Date of Birth", width=20, font="Modern 15")
    lbl.pack(side=LEFT)

    dob = ttk.DateEntry(master=cont, firstweekday=7)
    dob.pack(side=LEFT, fill=X)

    form_entry("Phone", phone, sign_frame, app.register(validate_phone))
    form_entry("Email", email, sign_frame, app.register(validate_email))
    state_comb = combo("State", sign_frame, list(all_states(csv_file)))

    # create button to go to the next set of user input
    btn_row = ttk.Frame(sign_frame)
    btn_row.pack(fill=X, expand=YES, pady=20)
    in_btn = ttk.Button(
        master=btn_row,
        text="Next",
        command=lambda: next_med(sign_frame, app, first_name, last_name, email, phone, dob, state_comb,
                                 network, csv_file),
        width=8
    )
    in_btn.pack(padx=5)

    app.mainloop()


def next_med(frame: ttk.LabelFrame, app: ttk.Toplevel, first_name: ttk.StringVar, last_name: ttk.StringVar,
             email: ttk.StringVar, phone: ttk.StringVar, dob: ttk.DateEntry, state: ttk.Combobox,
             network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the next set of information that the user inputs when creating an account.
    """
    if all([validate_text(first_name.get()), validate_text(last_name.get()), validate_email(email.get()),
            validate_phone(phone.get())]):
        # clear the frame
        for widgets in frame.winfo_children():
            widgets.pack_forget()

        # reformat the size of the window
        app.geometry('525x520')

        # reformat the frame
        frame.config(text='Medical Information')

        # form variables
        languages = ttk.StringVar(value="")
        prior_med = ttk.StringVar(value="")
        allergies = ttk.StringVar(value="")

        # create the inputs
        form_entry("Primary Language", languages, frame, app.register(validate_text))
        sex_comb = combo("Sex", frame, ['Female', 'Male', 'Intersex'])
        gender_comb = combo("Gender Identity", frame, ['Woman', 'Man', 'Trans Woman', 'Trans Man', 'Non-Binary',
                                                       'Other'])
        height_comb = combo("Height (cm)", frame, list(range(1, 301)))
        weight_comb = combo("Weight (kg)", frame, list(range(1, 301)))
        form_entry("Prior Medication", prior_med, frame, app.register(validate_text))
        form_entry("Allergies", allergies, frame, app.register(validate_text))

        # create button to go to the next set of user input
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill=X, expand=YES, pady=20)
        in_btn = ttk.Button(
            master=btn_row,
            text="Next",
            command=lambda: next_user(frame, app, first_name, last_name, email, phone, dob, state, languages, sex_comb,
                                      gender_comb, height_comb, weight_comb, prior_med, allergies, network, csv_file),
            width=8
        )
        in_btn.pack(padx=5)


def next_user(frame: ttk.LabelFrame, app: ttk.Toplevel, first_name: ttk.StringVar, last_name: ttk.StringVar,
              email: ttk.StringVar, phone: ttk.StringVar, dob: ttk.DateEntry, state: ttk.Combobox,
              languages: ttk.StringVar, sex: ttk.Combobox, gender: ttk.Combobox, height: ttk.Combobox,
              weight: ttk.Combobox, prior_med: ttk.StringVar, allergies: ttk.StringVar, network: HealthNetwork,
              csv_file: str) -> None:
    """
    This function creates the final username and password input screen for patient sign up.
    """
    if all([validate_text(languages.get()), validate_text(prior_med.get()), validate_text(allergies.get())]):
        # clear the frame
        for widgets in frame.winfo_children():
            widgets.pack_forget()

        # reformat the size of the window
        app.geometry('525x350')

        # reformat the frame
        frame.config(text='Privacy Information')

        # form variables
        user = ttk.StringVar(value="")
        passw = ttk.StringVar(value="")

        form_entry("Username", user, frame, app.register(validate_length))
        form_entry("Password", passw, frame, app.register(validate_length))

        # create button to sign up
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill=X, expand=YES, pady=30)
        up_btn = ttk.Button(
            master=btn_row,
            text="Sign Up",
            command=lambda: sign_up_btn(app, first_name, last_name, phone, email, sex, gender, languages, prior_med,
                                        allergies, user, passw, dob, state, height, weight, network, csv_file),
            width=8
        )
        up_btn.pack(padx=5)


def sign_up_btn(app: ttk.Toplevel, first_name: ttk.StringVar, last_name: ttk.StringVar,
                phone: ttk.StringVar, email: ttk.StringVar, sex: ttk.Combobox,
                gender: ttk.Combobox,
                languages: ttk.StringVar, prior_med: ttk.StringVar, allergies: ttk.StringVar,
                user: ttk.StringVar, passw: ttk.StringVar, dob: ttk.DateEntry,
                state_comb: ttk.Combobox, height_comb: ttk.Combobox,
                weight_comb: ttk.Combobox, network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the patient interface after a new patient is created.
    """
    if validate_length(user.get()) and validate_length(passw.get()):
        app.withdraw()
        new_patient = ttk.Toplevel(title='Patient')
        new_patient.geometry('800x650')

        # get values from parameters
        val_name1 = first_name.get()
        val_name2 = last_name.get()
        val_phone = phone.get()
        val_email = email.get()
        val_sex = sex.get()
        val_gender = gender.get()
        val_languages = languages.get()
        val_med = prior_med.get()
        val_allergies = allergies.get()
        val_user = user.get()
        val_passw = passw.get()
        val_dob = dob.entry.get()
        val_state = state_comb.get()
        val_height = height_comb.get()
        val_weight = weight_comb.get()

        val_dob_list = val_dob.split('/')
        val_dob_tup = (int(val_dob_list[0]), int(val_dob_list[1]), int(val_dob_list[2]))

        if val_med is not None:
            val_med = val_med.split(', ')

        if allergies is not None:
            val_allergies = val_allergies.split(', ')

        # create a patient from the given data
        pat = Patient(first_name=val_name1, last_name=val_name2, state=val_state, date_of_birth=val_dob_tup,
                      gender=val_gender, height=float(val_height), weight=float(val_weight),
                      language=val_languages, email=val_email, phone_number=int(val_phone),
                      prior_medication=val_med, allergies=val_allergies, username=val_user, password=val_passw,
                      sex=val_sex, diagnosis=None, current=None)

        # write the new patient into the csv file
        file = open('../Course Project/patient_info.csv', 'a')
        file.write(pat.to_string())
        file.write('\n')
        file.close()

        al_file = open('../Course Project/patient_allergies.csv', 'a')
        al_file.write(f'{pat.username}')
        al_file.write(',' + ','.join(pat.allergies))
        al_file.write('\n')
        al_file.close()

        med_file = open('../Course Project/patient_medication.csv', 'a')
        med_file.write(f'{pat.username}')
        med_file.write(',' + ','.join(pat.prior_medication))
        med_file.write('\n')
        med_file.close()

        # create label
        lbl_sign = ttk.Label(new_patient, text="Patient", font='Modern 30 bold')
        lbl_sign.pack(pady=30)

        my_note = ttk.Notebook(new_patient)
        my_note.pack(pady=40, fill=BOTH, anchor=N, padx=30)

        pat_info = ttk.Frame(my_note)
        doct = ttk.Frame(my_note)
        diagno = ttk.Frame(my_note)

        my_note.add(pat_info, text='Account')
        my_note.add(doct, text='Your Doctor')
        my_note.add(diagno, text='Diagnosis')

        # create label for find doctor
        lbl_doc = ttk.Label(doct, text="Request a Doctor Now!", font='Modern 30 bold')
        lbl_doc.pack(pady=30)

        # create button to find doctor
        btn_row = ttk.Frame(doct)
        btn_row.pack(fill=X, expand=YES, pady=30)
        doc_b = ttk.Button(
            master=btn_row,
            text="Search",
            command=lambda: find_doctor(csv_file, network, pat),
            width=8
        )
        doc_b.pack(padx=5)

        # Add diagnosis information
        lbl_doc = ttk.Label(diagno, text="No Diagnosis Yet", font='Modern 20 bold')
        lbl_doc.pack(pady=30)

        # Add Patient info to the Screen
        info_row(pat_info, f'Name: {pat.first_name} {pat.last_name}')
        info_row(pat_info, f'State: {pat.state}')
        info_row(pat_info, f'Date of Birth: {pat.date_of_birth[0]}/{pat.date_of_birth[1]}/{pat.date_of_birth[2]}')
        info_row(pat_info, f'Sex: {pat.sex}')
        info_row(pat_info, f'Gender: {pat.gender}')
        info_row(pat_info, f'Height: {pat.height} cm')
        info_row(pat_info, f'Weight: {pat.weight} kg')
        info_row(pat_info, f'Language: {pat.language}')
        info_row(pat_info, f'Email: {pat.email}')
        info_row(pat_info, f'Phone: {pat.phone_number}')
        info_row(pat_info, 'Medication: ' + ', '.join(pat.prior_medication))
        info_row(pat_info, 'Allergies: ' + ', '.join(pat.allergies))

        new_patient.mainloop()


def sign_in(app1: ttk.Window, network: HealthNetwork, csv_file: str) -> None:
    """
    This function creates the sign in page for Patients and Doctors
    """
    # close window
    app1.withdraw()

    # create sign in page
    app = ttk.Toplevel(title='Sign In')
    app.geometry('400x475')

    # create label
    lbl_sign = ttk.Label(app, text="Sign In", font='Modern 50 bold')
    lbl_sign.pack(pady=30)

    # create frame
    sign_frame = ttk.LabelFrame(app, text='Patient', padding=10)
    sign_frame.pack(fill=X, anchor=N, padx=30)

    # create username entry
    user_row = ttk.Frame(sign_frame)
    user_row.pack(fill=X, expand=YES)
    user_lbl = ttk.Label(user_row, text="Username", width=8)
    user_lbl.pack(side=LEFT, padx=(15, 0))
    user_var = ttk.StringVar(value="")
    user_ent = ttk.Entry(user_row, textvariable=user_var, validatecommand=lambda: validate_length(user_var.get()),
                         validate='focus')
    user_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # create password entry
    pass_row = ttk.Frame(sign_frame)
    pass_row.pack(fill=X, expand=YES, pady=15)
    pass_lbl = ttk.Label(pass_row, text="Password", width=8)
    pass_lbl.pack(side=LEFT, padx=(15, 0))
    pass_var = ttk.StringVar(value="")
    pass_ent = ttk.Entry(pass_row, textvariable=pass_var, validatecommand=lambda: validate_length(pass_var.get()),
                         validate='focus')
    pass_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # create button to login
    btn_row = ttk.Frame(sign_frame)
    btn_row.pack(fill=X, expand=YES, pady=30)
    in_btn = ttk.Button(
        master=btn_row,
        text="Sign In",
        command=lambda: sign_in_btn(app, user_var, pass_var, network, csv_file),
        width=8
    )
    in_btn.pack(padx=5)

    # create text for doctor login
    lbl_doc = ttk.Label(app, text="Are you a doctor?", font='Modern 20')
    lbl_doc.pack(pady=20)

    # create button for doctor login
    in_btn = ttk.Button(
        master=app,
        text="Doctor Sign In",
        command=lambda: sign_in_doctor(app, network, csv_file),
        width=12
    )
    in_btn.pack()

    app.mainloop()


def sign_in_btn(app: ttk.Toplevel, user: ttk.StringVar, passw: ttk.StringVar, network: HealthNetwork,
                csv_file: str) -> None:
    """
    This function creates the patient window for patients that sign in
    """
    row = check_user(user.get(), '../Course Project/patient_info.csv')

    if row is not None and check_pass(passw.get(), row):
        app.withdraw()
        patient_win = ttk.Toplevel(title='Patient')
        patient_win.geometry('800x650')

        pat_aller = check_user(row[0], '../Course Project/patient_allergies.csv')
        pat_med = check_user(row[0], '../Course Project/patient_medication.csv')

        aller_list = [pat_aller[x] for x in range(len(pat_aller)) if x != 0]
        med_list = [pat_med[x] for x in range(len(pat_med)) if x != 0]

        # create patient from csv since patient has no doctor
        pat = Patient(
            first_name=row[2],
            last_name=row[3],
            state=row[4],
            date_of_birth=(int(row[5]), int(row[6]), int(row[7])),
            sex=row[8],
            gender=row[9],
            height=float(row[10]),
            weight=float(row[11]),
            language=row[12],
            email=row[13],
            phone_number=int(row[14]),
            prior_medication=med_list,
            allergies=aller_list,
            diagnosis=row[15],
            current=None,
            username=row[0],
            password=row[1]
        )

        # if the patient does have a doctor, find the existing patient attribute in the network
        if row[-1] is not None:
            for patient in network.patients:
                if patient.username == row[0] and patient.password == row[1]:
                    pat = patient

        # create label
        lbl_sign = ttk.Label(patient_win, text="Patient", font='Modern 30 bold')
        lbl_sign.pack(pady=30)

        my_note = ttk.Notebook(patient_win)
        my_note.pack(pady=40, fill=BOTH, anchor=N, padx=30)

        pat_info = ttk.Frame(my_note)
        doct = ttk.Frame(my_note)
        diagno = ttk.Frame(my_note)

        my_note.add(pat_info, text='Account')
        my_note.add(doct, text='Your Doctor')
        my_note.add(diagno, text='Diagnosis')

        if pat.current is None:
            # create label for find doctor
            lbl_doc = ttk.Label(doct, text="Request a Doctor Now!", font='Modern 30 bold')
            lbl_doc.pack(pady=30)

            # create button to find doctor
            btn_row = ttk.Frame(doct)
            btn_row.pack(fill=X, expand=YES, pady=30)
            doc_b = ttk.Button(
                master=btn_row,
                text="Search",
                command=lambda: find_doctor(csv_file, network, pat),
                width=8
            )
            doc_b.pack(padx=5)
        else:
            # Display Doctor information
            info_row(doct, f'Name: {pat.current.professional.first_name} {pat.current.professional.last_name}')
            if pat.current.professional.profession is True:
                info_row(doct, 'Profession: Psychologist')
            else:
                info_row(doct, 'Profession: Counselor')
            info_row(doct, f'Specialization: {pat.current.professional.specialization}')
            info_row(doct, f'Degree: {pat.current.professional.degree}')
            if pat.current.professional.gender == 'F':
                info_row(doct, 'Gender: Female')
            else:
                info_row(doct, 'Gender: Male')
            info_row(doct, f'State: {pat.current.professional.state}')
            info_row(doct, f'Email: {pat.current.professional.email}')
            info_row(doct, f'Phone: {pat.current.professional.phone_number}')

            # create label for finding a doctor
            lbl_doc = ttk.Label(doct, text="Request a New Doctor", font='Modern 20 bold')
            lbl_doc.pack(pady=30)

            # create button to find doctor
            btn_row = ttk.Frame(doct)
            btn_row.pack(fill=X, expand=YES, pady=30)
            doc_b = ttk.Button(
                master=btn_row,
                text="Search",
                command=lambda: find_doctor(csv_file, network, pat),
                width=8
            )
            doc_b.pack(padx=5)

        # Add diagnosis information
        if pat.diagnosis is not None:
            info_row(diagno, f'Diagnosis: {pat.diagnosis}')
        else:
            # create label
            lbl_doc = ttk.Label(diagno, text="No Diagnosis Yet", font='Modern 20 bold')
            lbl_doc.pack(pady=30)

        # Add Patient info to the Screen
        info_row(pat_info, f'Name: {pat.first_name} {pat.last_name}')
        info_row(pat_info, f'State: {pat.state}')
        info_row(pat_info, f'Date of Birth: {pat.date_of_birth[0]}/{pat.date_of_birth[1]}/{pat.date_of_birth[2]}')
        info_row(pat_info, f'Sex: {pat.sex}')
        info_row(pat_info, f'Gender: {pat.gender}')
        info_row(pat_info, f'Height: {pat.height} cm')
        info_row(pat_info, f'Weight: {pat.weight} kg')
        info_row(pat_info, f'Language: {pat.language}')
        info_row(pat_info, f'Email: {pat.email}')
        info_row(pat_info, f'Phone: {pat.phone_number}')
        info_row(pat_info, 'Medication: ' + ', '.join(pat.prior_medication))
        info_row(pat_info, 'Allergies: ' + ', '.join(pat.allergies))

        patient_win.mainloop()


def find_doctor(csv_file: str, network: HealthNetwork, pat: Patient) -> None:
    """
    Find a doctor for the given patient.
    """
    find_doc = ttk.Toplevel(title='Find A Doctor')
    find_doc.geometry('400x400')

    # create label
    lbl_sign = ttk.Label(find_doc, text="Find a Doctor", font='Modern 50 bold')
    lbl_sign.pack(pady=30)

    # create frame
    doc_frame = ttk.LabelFrame(find_doc, text='Find a Doctor', padding=10)
    doc_frame.pack(fill=X, anchor=N, padx=30)

    lbl_doc = ttk.Label(doc_frame, text='Select your preferences below.')
    lbl_doc.pack()

    prof_comb = combo('Profession', doc_frame, ['Psychologist', 'Counselor'])

    # create button to find doctors
    btn_row = ttk.Frame(doc_frame)
    btn_row.pack(fill=X, expand=YES, pady=30)
    in_btn = ttk.Button(
        master=btn_row,
        text="Next",
        command=lambda: prof_btn(find_doc, network, csv_file, prof_comb, pat),
        width=8
    )
    in_btn.pack(padx=5)

    find_doc.mainloop()


def prof_btn(app: ttk.Toplevel, network: HealthNetwork, csv_file: str, prof_comb: ttk.Combobox, pat: Patient) -> None:
    """
    Asks the user for further specification
    """
    app.withdraw()

    doc_win = ttk.Toplevel(title='Select A Doctor')
    doc_win.geometry('400x400')

    # create label
    lbl_sign = ttk.Label(doc_win, text="Find a Doctor", font='Modern 50 bold')
    lbl_sign.pack(pady=30)

    # create frame
    doc_frame = ttk.LabelFrame(doc_win, text='Find a Doctor', padding=10)
    doc_frame.pack(fill=BOTH, anchor=N, padx=30)

    lbl_doc = ttk.Label(doc_frame, text='Select your preferences below.')
    lbl_doc.pack()

    spec_comb = combo('Specialization', doc_frame, list(get_specializations(csv_file, prof_comb.get())))
    state_comb = combo("State", doc_frame, list(all_states(csv_file)))

    # create button to find doctors
    btn_row = ttk.Frame(doc_frame)
    btn_row.pack(fill=X, expand=YES, pady=30)
    in_btn = ttk.Button(
        master=btn_row,
        text="Search",
        command=lambda: doc_btn(doc_win, network, csv_file, prof_comb, spec_comb, state_comb, pat),
        width=8
    )
    in_btn.pack(padx=5)

    doc_win.mainloop()


def doc_btn(app: ttk.Toplevel, network: HealthNetwork, csv_file: str, prof_comb: ttk.Combobox, spec_comb: ttk.Combobox,
            state_comb: ttk.Combobox, pat: Patient) -> None:
    """
    Display the possible doctor that the patient can choose from
    """
    app.withdraw()
    doc = ttk.Toplevel(title='Select A Doctor')
    doc.geometry('400x600')

    lbl_sign = ttk.Label(doc, text="Select a Doctor", font='Modern 50 bold')  # create label
    lbl_sign.pack(pady=30)

    frame = ttk.LabelFrame(doc, text='Select a Doctor', padding=10)  # create frame
    frame.pack(fill=X, anchor=N, padx=30)

    possible_docs = list_filtered_doctors(csv_file, [['Classification', prof_comb.get()],
                                                     ['Specialization', spec_comb.get()], ['State', state_comb.get()]])

    if possible_docs:
        doctor = random.choice(possible_docs)  # Display randomly generated doctor
        info_row(frame, f'Name: {doctor.first_name} {doctor.last_name}')
        if doctor.profession is True:
            info_row(frame, 'Profession: Psychologist')
        else:
            info_row(frame, 'Profession: Counselor')
        info_row(frame, f'Specialization: {doctor.specialization}')
        info_row(frame, f'Degree: {doctor.degree}')
        if doctor.gender == 'F':
            info_row(frame, 'Gender: Female')
        else:
            info_row(frame, 'Gender: Male')
        info_row(frame, f'State: {doctor.state}')

        btn_row1 = ttk.Frame(frame)
        btn_row1.pack(fill=X, expand=YES, pady=30)
        yes_btn = ttk.Button(  # create accept button
            master=btn_row1,
            text="Accept",
            command=lambda: yes_opt(doc, pat, network, doctor),
            width=8
        )
        yes_btn.pack(padx=5)

        btn_row3 = ttk.Frame(frame)
        btn_row3.pack(fill=X, expand=YES, pady=30)
        cancel_btn = ttk.Button(  # create cancel button
            master=btn_row3,
            text="Cancel",
            command=lambda: cancel(doc),
            width=8
        )
        cancel_btn.pack(padx=5)
    else:
        lbl_no = ttk.Label(frame, text="No Doctor Available. Try Again!", font='Modern 20 bold')
        lbl_no.pack(pady=30)
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill=X, expand=YES, pady=30)
        cancel_btn = ttk.Button(  # create cancel button
            master=btn_row,
            text="Cancel",
            command=lambda: cancel(doc),
            width=8
        )
        cancel_btn.pack(padx=5)
    doc.mainloop()


def cancel(app: ttk.Toplevel) -> None:
    """
    Closes the page
    """
    app.withdraw()


def yes_opt(app: ttk.Toplevel, pat: Patient, network: HealthNetwork, doc: Medical) -> None:
    """
    The user selected yes to the doctor
    """
    for doctor in network.offices:
        if doctor.user == doc.user:
            network.offices[doctor].waitlist.append(pat)
    app.withdraw()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['patient_intake', 'database', 'ttkbootstrap', 'tkinter.constants', 'csv',
                          'random', 'interface_helpers'],
        'disable': ['too-many-arguments', 'too-many-locals', 'forbidden-IO-function',
                    'consider-using-with', 'too-many-statements', 'too-many-nested-blocks', 'possibly-undefined']
    })
