# tCF Developer Info

## Setup

1. Ensure your system has [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), Node, Python, PostgreSQL, and [Docker](https://docs.docker.com/install/) installed.
2. Clone the project:

```console
$ git clone https://github.com/thecourseforum/theCourseForum2.git
$ cd theCourseForum
```

3. Download the `.env` secrets file from the [secrets repo](https://github.com/thecourseforum/tCF-Secrets/blob/master/.env) and place it in the project root.
- _**Note**_: the file should be named exactly `.env`, not `.env.txt` or `env.txt` - rename if necessary.

4. Install python dependencies for your local environment:

```console
$ pip install -r requirements.txt
```

5. Install `pre-commit` to ensure your commit pasts formatting and linting:

```console
$ git config --unset-all core.hooksPath
$ pre-commit install
```

6. Build the project:

```console
$ docker compose up
```

7. Wait for the Django server to finish building (i.e. `tcf_django | Watching for file changes with StatReloader` is visible in stdout).
8. Download and place the [latest database backup](https://drive.google.com/drive/u/0/folders/1a7OkHkepOBWKiDou8nEhpAG41IzLi7mh) from Google Drive into `db/latest.sql` in your local repo.
9. Update the database according to your operating system:

MacOS/Linux:

```console
$ sh scripts/reset-db.sh db/latest.sql
```

Windows:

```console
$ scripts\reset-db.bat db/latest.sql
```

7. Ensure the website is up, running, and functional at `localhost:8000`.

## [Useful Commands](docs/useful-commands.md)

## Common Issues

- Docker build error `=> CANCELED [internal] load build context`
  - This occurs because of a Windows compatibility issue with Docker. As of December 19, 2023, downgrade Docker to [version 4.19](https://docs.docker.com/desktop/release-notes/#4190), then re-build the project.

## Stack

The application stack is listed below. These technologies were chosen because they are robust and align with the stack that UVA students learn in courses.

- Python
- Django
- PostgreSQL
- Bootstrap 4
- Javascript (jQuery)