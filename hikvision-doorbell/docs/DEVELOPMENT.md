# Development guide

The current setup only works for x86/x64 system due to the HikVision SDK native libraries used, and has been tested on a Linux OS (Linux Mint).

## Requirements

- Python 3.10
- (recommended) A fresh [virtualenv](https://docs.python.org/3/library/venv.html) for this project

## Instructions
After having cloned the repository, run the following commands from the `hikvision-doorbell` directory.

- Install the project development dependencies
```bash
pip install -r requirements.dev.txt
```

- Export the required environment variables to configure the software (see `development.env.example` for reference)
```bash
export DOORBELLS='[{"name":"outdoor", "ip": "192.168.0.1", "username": "user", "password": "password"}]'
export HOME_ASSISTANT__URL=http://localhost:8123
export HOME_ASSISTANT__TOKEN=<secret_token>
```

- Launch the application
```bash
python src/main.py
```

## VSCode

If using VSCode, there is a run configuration already provided.
- First create a `development.env` file with your own values, then run the application using the integrated VSCode debugger.
```bash
cp development.env.example development.env
```

- Run the application using the integrated VSCode runner (under `Run and Debug`).

## Testing the add-on locally (VSCode devcontainer)

For more information see the official HA [guide](https://developers.home-assistant.io/docs/add-ons/testing).

Inside the _devcontainer_ use the task `Start Home Assistant` to bootstrap the HA supervisor, who will then proceed to locally install HA.

The local instance is accessible under `http://localhost:7123/`.

The addon should be visible in the add-on store.

## Contributing

This project used [pre-commit](https://pre-commit.com/) hooks to run pre-commit `git` hooks.
The firs time you clone this repo, please run `pre-commit install` at the root of the repository to enable automatic handling of the `git` pre-commit scripts. This won't affect any of your other repositories, just this one.
Their configuration is managed in [.pre-commit-config.yaml](/.pre-commit-config.yaml).

## Release

The release process is automated using Github Actions.
See the [workflow file](/.github/workflows/deploy.yml) for the definition of the automated steps.

The manual steps to publish a new release are as follows:
1. `git checkout` the branch containing the release code
2. Update the `CHANGELOG.md` file as appropriate 
   
   Update the `config.yaml`->`version` to point to the new version
3. `git commit` the changes
3. `git tag` using the format `<name of the addon>-<version number>`
    
    e.g: `git tag doorbell-v3.0.0` to release version `3.0.0` of the addon `doorbell`
4. `git push --tags` to push the tags to the repository and start the automatic release process

## Project structure

The Python project is described via the standard `pyproject.toml` file, containing all its metadata, such as its name, description and dependencies.

### Dependencies

The Python dependencies are declared inside the `pyproject.toml` file.
However, as [this detailed post](https://caremad.io/posts/2013/07/setup-vs-requirement/) explains, when developing a Python application it is good practice to _pin_ the specific version of dependencies the application has been tested and built with, to ensure a consistent runtime behavior when deployed.

To this ends, [pip-compile](https://pip-tools.readthedocs.io/en/latest/) is used to generate various `requirements.txt` files containing the specific versions of dependencies used, separating between both production and development environments.
Refer to each file to see the command that was used to generate it.