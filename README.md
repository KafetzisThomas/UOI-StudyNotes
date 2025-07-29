<div align="center">
  <h1>UOI-StudyNotes</h1>
  <p>
    <b>A notes archive app for UOI students.</b><br>
    Written in Python/Django.
  </p>
</div>

## Overview

<details open>
<summary>Greek Edition</summary>
<br>

Το `UOI-StudyNotes` είναι μια web εφαρμογή **αρχειοθέτησης σημειώσεων** για φοιτητές του Πανεπιστημίου Ιωαννίνων ώστε να `μοιράζονται`, να έχουν `πρόσβαση` και να `συνεργάζονται` σε ακαδημαϊκές σημειώσεις διαφόρων μαθημάτων.

</details>

<details closed>
<summary>English Edition</summary>
<br>

`UOI-StudyNotes` is a **notes archive** app for UOI students to `share`, `access` and `collaborate` on academic notes across various subjects.

</details>

## Django Models

![Django Models Graph](https://github.com/user-attachments/assets/0933c9db-9f23-49d0-a89a-c17e098d2fb2)

## Setup for Local Development

### Install uv

```bash
cd path/to/root/directory
pip install uv
```

### Create Enviroment Variable file

```bash
touch main/.env
nano main/.env
```

Add the following (adjust as needed):

```ini
# Django settings
SECRET_KEY="example_secret_key"  # https://stackoverflow.com/a/57678930
ALLOWED_HOSTS="localhost,127.0.0.1"
CSRF_TRUSTED_ORIGINS="http://localhost:8001"
DEBUG=True  # For development

# Email settings
EMAIL_HOST_USER="example_email_host"
EMAIL_HOST_PASSWORD="example_email_password"
```

Save changes and close the file.

### Migrate Database

```bash
uv run manage.py migrate
```

### Run Django Server

```bash
uv run manage.py runserver
```

Access web application at `http://127.0.0.1:8000` or `http://localhost:8000`.

## Run Tests

```bash
uv run manage.py test
```

## Contributing Guidelines

<details open>
<summary>Greek Edition</summary>
<br>

### Pull Requests

- **Απλότητα**: Κρατήστε τις αλλαγές σας απλές, στοχευμένες και εύκολες προς ανασκόπηση.
- **Βιβλιοθήκες**: Αποφύγετε την προσθήκη μη τυπικών βιβλιοθηκών. Αν είναι απαραίτητο δημιουργήστε πρώτα ένα GitHub issue για αξιολόγηση.
- **Έλεγχος**: Βεβαιωθείτε ότι ο κώδικας εκτελείται χωρίς σφάλματα, περνά όλα τα tests και τηρεί τα πρότυπα κώδικα.

### Αναφορές Σφαλμάτων

- Υποβάλετε σφάλματα μέσω των GitHub Issues.
- Υποβάλετε pull requests μέσω των GitHub Pull Requests.

Ευχαριστούμε για την υποστήριξη του UOI-StudyNotes!

</details>

<details closed>
<summary>English Edition</summary>
<br>

### Pull Requests

- **Simplicity**: Keep changes focused and easy to review.
- **Libraries**: Avoid adding non-standard libraries unless discussed via an issue.
- **Testing**: Ensure code runs error-free, passes all tests, and meets coding standards.

### Bug Reports

- Report bugs via GitHub Issues.
- Submit pull requests via GitHub Pull Requests.

Thank you for supporting UOI-StudyNotes!

</details>
