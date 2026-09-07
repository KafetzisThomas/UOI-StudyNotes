<div align="center">
    <img src="static/favicon.png" width="150"/>
    <p><strong>UOI-StudyNotes: </strong>A notes archive app for UOI students.<br>Written in Python/Django</p>
    <img src="https://github.com/KafetzisThomas/UOI-StudyNotes/actions/workflows/tests.yml/badge.svg"/>
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

## Database Schema

![Database Schema](/assets/db_schema.png)

## Usage

First install `uv` and sync the project dependencies:

```bash
cd path/to/root/directory
pip install uv
uv sync
uv sync --group dev  # for devs only
```

Migrate database:

```bash
uv run manage.py migrate
```

Run Django server:

```bash
uv run manage.py runserver
```

Access web application at `http://127.0.0.1:8000` or `http://localhost:8000`.

## Run Tests

```bash
uv run manage.py test
```
