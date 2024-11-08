<div align="center">
    <h1>UOI-StudyNotes</h1>
    <p>
        A notes archive app for UOI students.<br>
        Written in Python/Django
    </p>
    <a href="https://github.com/KafetzisThomas/UOI-StudyNotes/actions/workflows/tests.yml">
        <img src = "https://github.com/KafetzisThomas/UOI-studyNotes/actions/workflows/tests.yml/badge.svg" alt="Run Tests"/>
    </a>
</div>

---

## Overview

<details open>
<summary>Greek Edition</summary>
<br>

Το `UOI-StudyNotes` είναι μια web εφαρμογή **αρχειοθέτησης σημειώσεων** για φοιτητές του Πανεπιστημίου Ιωαννίνων, ώστε να `μοιράζονται`, να έχουν `πρόσβαση` και να `συνεργάζονται` σε ακαδημαϊκές σημειώσεις διαφόρων μαθημάτων.

</details>

<details closed>
<summary>English Edition</summary>
<br>

`UOI-StudyNotes` is a **notes archive** app for UOI students to `share`, `access`, and `collaborate` on academic notes across various subjects.

</details>

## Django Models
Here is a graphical representation of the Django models used in this project:

<div align="center"><img src="https://github.com/user-attachments/assets/0933c9db-9f23-49d0-a89a-c17e098d2fb2" alt="Django Models Graph" width="500"/></div>

## Setup for Local Development

### Set up Virtual Environment

```bash
➜ cd path/to/root/directory
$ python3 -m venv env/
$ source env/bin/activate
```

### Install Dependencies

```bash
$ pip3 install -r requirements.txt
```

### Create Enviroment Variable file

```bash
$ touch main/.env
$ nano main/.env
```

Add the following environment variables (modify as needed):
```bash
➜ SECRET_KEY="example_secret_key"  # https://stackoverflow.com/a/57678930
➜ DEBUG=True  # For development
```

Save changes and close the file.

<blockquote>
Note: If you prefer, you can run the application using Docker by running:<br><br>

`$ docker compose up`
</blockquote>

### Migrate Database

```bash
$ python3 manage.py migrate
```

### Run Django Server
```bash
$ python3 manage.py runserver
```

Now you can access the website at `http://127.0.0.1:8000/` or `http://localhost:8000/`.

## Run Tests

```bash
➜ cd path/to/root/directory
$ python3 manage.py test notes.tests users.tests
```

## Contributing Guidelines for UOI-StudyNotes

<details open>
<summary>Greek Edition</summary>
<br>

### Pull Requests
Όταν υποβάλετε ένα pull request, θυμηθείτε τα εξής:

* **TODO λίστα**: Eλέγξτε τη [TODO λίστα](https://github.com/KafetzisThomas/UOI-StudyNotes/blob/main/TODO.md) για να βεβαιωθείτε ότι δεν υπάρχει ήδη κάποια ανοιχτή εργασία που θα θέλατε να αναλάβετε (μόνο Αγγλικά λόγω των τεχνικών αναφορών).

* **Διατηρήστε το απλό**: Προτιμήστε να κρατάτε τις αλλαγές σας απλές και στοχευμένες. Οι πιο σύνθετες αλλαγές είναι δυσκολότερο να ελεγχθούν και να ενσωματωθούν.

* **Αποφύγετε την προσθήκη νέων βιβλιοθηκών**: Αν γίνεται, προσπαθήστε να μην προσθέσετε νέες βιβλιοθήκες που δεν είναι τυπικές. Εάν αυτό είναι αποχρεωτικό, παρακαλώ δημιουργήστε πρώτα ένα github issue για να αξιολογηθεί η χρησιμότητα και η συμβατότητά του.

* **Σιγουρευτείτε ότι λειτουργεί**: Πριν υποβάλετε ένα pull request, βεβαιωθείτε ότι ο κώδικάς σας εκτελείται χωρίς σφάλματα και ότι ακολουθεί τα πρότυπα κωδικοποίησης του έργου.

* **Εκτελέστε τις δοκιμές**: Βεβαιωθείτε ότι όλες οι υπάρχουσες [δοκιμές](#run-tests) ολοκληρώνονται επιτυχώς και προσθέστε νέες αν χρειαστεί. Τα pull requests σας δεν θα εγκριθούν αν δεν περάσουν όλες οι δοκιμές.

### Αναφορά Σφαλμάτων και Pull Requests
Αν εντοπίσετε κάποιο σφάλμα, παρακαλούμε ακολουθήστε τα παρακάτω βήματα:

* **Αναφορά σφαλμάτων**: Υποβάλετε τις αναφορές σας στην [GitHub Issues](https://github.com/KafetzisThomas/UOI-StudyNotes/issues) σελίδα.
* **Pull Requests**: Ανοίξτε ένα pull request στην [GitHub Pull Requests](https://github.com/KafetzisThomas/UOI-StudyNotes/pulls) σελίδα.

Πριν συμβάλετε, ρίξτε μια ματιά στην [άδεια](https://github.com/KafetzisThomas/UOI-StudyNotes/blob/main/LICENSE) για να κατανοήσετε τους όρους και τις προϋποθέσεις που διέπουν στη χρήση του UOI-StudyNotes.

Ευχαριστούμε για το ενδιαφέρον σας στο να βελτιώνετε το UOI-StudyNotes!

</details>

<details closed>
<summary>English Edition</summary>
<br>

### Pull Requests
When submitting a pull request, please keep these points in mind:

* **TODO List**: Check the [TODO List](https://github.com/KafetzisThomas/UOI-StudyNotes/blob/main/TODO.md) to ensure there isn’t already an open task you’d like to work on.

* **Simplicity**: Keep your changes straightforward and focused. Complex changes are harder to review and integrate.

* **Avoid Non-Standard Libraries**: Whenever possible, refrain from adding new non-standard libraries. If your idea necessitates one, kindly discuss it first by opening an issue. This helps in evaluating the necessity and compatibility of the library.

* **Ensure It Runs**: Before submitting a pull request, ensure that your code runs without errors and adheres to the project's coding standards.

* **Pass All Tests**: Make sure all existing [tests](#run-tests) pass and add new tests as necessary. Pull requests will not be merged unless all tests pass successfully.

### Filing Bug Reports and Submitting Pull Requests
If you encounter a bug, please follow these steps to report it:

* **Bug Reports**: File bug reports on the [GitHub Issues](https://github.com/KafetzisThomas/UOI-StudyNotes/issues) page.
* **Pull Requests**: Open pull requests on the [GitHub Pull Requests](https://github.com/KafetzisThomas/UOI-StudyNotes/pulls) page.

Before contributing, please review the [License](https://github.com/KafetzisThomas/UOI-StudyNotes/blob/main/LICENSE) to understand the terms and conditions governing the use and distribution of UOI-StudyNotes.

Thank you for your interest in improving UOI-StudyNotes!

</details>
