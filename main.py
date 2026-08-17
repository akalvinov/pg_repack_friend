import os
import subprocess
from pydantic import BaseModel
import yaml
from datetime import datetime

start_time = datetime.today().strftime('%Y-%m-%d-%H-%M')
report_file = f"report-{start_time}.log"
log_file = f"log-{start_time}.log"

class PGCluster(BaseModel):
    # Структура для валидации yaml конфига
    host: str
    port: int
    db: str
    user: str
    password: str
    tables: list[str]

class Config(BaseModel):
    # Структура для валидации yaml конфига
    repack_cmd: str
    clusters: list[PGCluster]

def report(message: str):
    # Простая функция дублирования вывода на экран и в файл отчета
    print(message)
    with open(report_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')


def get_tablesize(cluster: PGCluster, table: str) -> str:
    env = os.environ.copy()
    env['PGPASSWORD'] = cluster.password
    args = [
        'psql',
        '-h', cluster.host,
        '-p', str(cluster.port),
        '-U', cluster.user,
        '-d', cluster.db,
        '-t',
        '-c', "SELECT pg_size_pretty(pg_total_relation_size('{}'));".format(table)
    ]
    try:
        result = subprocess.run(args, env=env, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        report(f"Failed to get size of cluster {cluster.host}, table {t} with error: {e.stderr}")
        exit(1)


def run_repack(repack_cmd: str, cluster: PGCluster, table: str) -> str:
    env = os.environ.copy()
    env['PGPASSWORD'] = cluster.password
    args = [
        repack_cmd,
        '--host', cluster.host,
        '--port', str(cluster.port),
        '--dbname', cluster.db,
        '--username', cluster.user,
        '--table', table,
        '--no-password',
        '--no-superuser-check',
        '--echo'
    ]
    try:
        with open(log_file, 'a', encoding='utf-8') as file:
            result = subprocess.run(args, env=env, check=True,  text=True, stderr=file)
            return result.stdout
    except subprocess.CalledProcessError as e:
        report(f"Failed to run repack of cluster {cluster.host} - {cluster.db}, table {t} with error: {e.stderr}")
        exit(1)


with open('config.yaml', 'r') as f:
    raw_data = yaml.load(f, Loader=yaml.SafeLoader)
    config = Config(**raw_data)
    report(f"Realtime logs are in {log_file}")
    for cluster in config.clusters:
        for t in cluster.tables: 
            report(f"Running for cluster {cluster.host}, table {t}")
            result = get_tablesize(cluster, t)
            report(f"Size before: {result}")
            result = run_repack(config.repack_cmd,cluster, t)
            result = get_tablesize(cluster, t)
            report(f"Size after: {result}")
