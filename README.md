# vault-loadtester
This repo is a collection of python scripts that i use to run a multithreaded load on Vault. There is limted to no error handeling, use at own risk.

## Dependancies
- Python3
- pip

## Activate
```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Deactivate
```bash
deactivate
```

## Usage
Start a Vault dev instance
```bash
vault server -dev -dev-root-token-id=dev
```

Set the env vars so `vault-loadtester` knows how to reach Vault
```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=dev
```

This script expects the following to be configured in Vault
- The transit engine to be mounted at `/transit`
- An encryption key to already be created and its name passed with `--key <keyname>`

Run transit test
```bash
./vault-loadtester --key test --duration 10
```

Help menu
```bash
./vault-loadtester -h
usage: vault-loadtest [-h] [--threads [THREADS]] [--key [KEY]] [--duration [DURATION]] [-v]

Non-Function Load Testing of Vault

optional arguments:
  -h, --help            show this help message and exit
  --threads [THREADS]   How many threads should be used.
  --key [KEY]           What is the name of the encryption key to use.
  --duration [DURATION]
                        Duration of the test
  -v, --verbosity       Increase logging verbosity with more --vv
```

Example run
```bash
./vault-loadtester --key test --duration 10
19-Oct-21 08:11:31 19474 WARNING - Log level set to WARNING
Requests per second 555.0
Number of Reqests 5550
Number of 200s 5550
Mean = 0.00687 seconds
90%  = 0.00894 seconds
95%  = 0.00954 seconds
99%  = 0.01105 seconds
```

