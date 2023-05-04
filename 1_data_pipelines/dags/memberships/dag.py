from datetime import datetime
from airflow.decorators import dag, task


@dag(start_date=datetime(2023, 1, 1), schedule_interval="@hourly", catchup=False)
def memberships_approval():
    requirements = ["polars[pandas,pyarrow]~=0.17.11"]

    @task.virtualenv(requirements=requirements)
    def process_memberships(ts=None):
        from memberships.helpers import load_data, process_data, save_data

        if ts is None:
            ts = datetime(2023, 1, 1).isoformat()

        input_pattern = "input/*.csv"
        output_path = "output"

        df = load_data(input_pattern, ts)
        processed_df = process_data(df)
        save_data(processed_df, output_path)

    process_memberships_task = process_memberships()


memberships_approval_dag = memberships_approval()
