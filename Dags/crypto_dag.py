from datetime import datetime, timedelta
import requests
import pandas as pd
from airflow import DAG
from airflow.decorators import task
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from airflow.providers.postgres.hooks.postgres import PostgresHook

conn = 'crypto_postgres'

default_args = {
    "owner": "crypto API data",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


profile_config = ProfileConfig(
    profile_name="crypto_dbt",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=conn,
        profile_args={"schema": "silver"}, 
    ),
)
with DAG(
    dag_id="crypto_bronze_ingestion",
    default_args=default_args,
    description="Ingest Raw Crypto Data from CoinGecko API to Bronze Layer",
    schedule="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag: 
    
    @task
    def create_bronze_sc():
        hook = PostgresHook(postgres_conn_id=conn)

        init_sql = """
        CREATE SCHEMA IF NOT EXISTS silver;
        CREATE SCHEMA IF NOT EXISTS gold;
        """
        hook.run(init_sql)

    @task
    def fetch_and_load():
        url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": "usd",
            "ids": "bitcoin,ethereum,solana,binancecoin",
            "order": "market_cap_desc"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from API: {response.text}")
        
        data = response.json()

        df = pd.DataFrame(data)
        df_filtered = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]

        hook = PostgresHook(postgres_conn_id=conn)
        connection = hook.get_sqlalchemy_engine()

        df_filtered.to_sql(
            name="raw_crypto_market_data",
            con=connection,
            schema="bronze",
            if_exists="append",
            index=False
        )

    dbt_transformations = DbtTaskGroup(
        group_id="dbt_medallion_transformations",
        project_config=ProjectConfig("/usr/local/airflow/dbt/crypto_dbt"),
        profile_config=profile_config,
    )

    create_bronze = create_bronze_sc()
    fetch_and_loading = fetch_and_load()
    
    create_bronze >> fetch_and_loading >> dbt_transformations