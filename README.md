## pg_repack assistant

This python script helps runnibg pg_repack in batch.

List all postgresql cluster and corresponding database in config.yaml and run script to repack all databases sequentially. 

## Usage

### Prerequirements

- psql
- pg_repack
- python3

### Venv and dependencies

Init venv
```
python -m venv venv 
```
activate venv
```
source venv/bin/activate
```
install dependencies 
```
pip3 install -r requirements.txt
```

### Configure and run

Edit config.yaml.example to your needs and save it as config.yaml.

Run

```
python main.py
```

To see progress run

```
tail -f name-of-log-file 
```