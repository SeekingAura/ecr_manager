## Module requirements
Requirements are separated by OS and check compatibility for these:
- Windows 10 (Windows)
- Ubuntu 22.04 LTS (Linux)

### Windows
#### Functional requirements
To install ONLY the functional requirements install from **requirements.txt**:
```bash
python -m pip install -r ".\requirements\windows\requirements.txt"
```

#### Stubs requirements
To install stubs ONLY install from **stub.txt**:
```bash
python -m pip install -r ".\requirements\windows\stubs.txt"
```
## Config CLI
### Env vars
Before to run must config env vars (just follow *.env-template* file)

#### AWS Vars
- **AWS_ACCESS_KEY_ID**: Acces key ID that identifies the **IAM**
- **AWS_SECRET_ACCESS_KEY**: Secret Access key required for authentication
- **AWS_DEFAULT_REGION**: Region where AWS resources are located, for ECR service check here https://docs.aws.amazon.com/general/latest/gr/ecr.html

#### Python vars
- **LOG_LEVEL**: General log level at Run application, one of standard values defined here https://docs.python.org/3/library/logging.html#logging-levels

### Data input
input for application via files, follow content of folder **data_input-template**.

#### images_data.json
By default CLI expects the file **images_data.json**, in a new releases can use multiple files

## Run
### CLI
To execute with default config run:
```
python ecr_manager
```

This run **ecr_manager/__main__.py**, new releases will have parameters, and possibility of GUI

# License
This repository contains MIT License (MIT). See [License](/LICENSE) for more information.
