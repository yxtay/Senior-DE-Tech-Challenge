from datetime import datetime
from airflow.decorators import dag, task


@dag(start_date=datetime(2023, 1, 1), schedule_interval="@hourly", catchup=False)
def memberships_pipeline():
    @task()
    def process_memberships(ts=None):
        import hashlib
        from pathlib import Path

        import polars as pl

        def load_data(data_csv_pattern: str, ts: str) -> pl.DataFrame:
            csv_paths = Path(".").glob(data_csv_pattern)
            assert len(csv_paths) > 0, f"no file found: {data_csv_pattern}"

            df = pl.concat(pl.scan_csv(csv) for csv in csv_paths).with_columns(
                pl.lit(ts[:10]).alias("ds"),
                pl.lit(ts).alias("ts"),
            )

            n_rows, _ = df.collect().shape
            assert n_rows > 0, "no data loaded"

            expected_cols = set(["name", "email", "date_of_birth", "mobile_no"])
            check_columns = len(expected_cols & set(df.columns)) == len(expected_cols)
            msg = f"missing columns, expected: {expected_cols}, actual: {df.columns}"
            assert check_columns, msg

            return df

        def process_name(df: pl.DataFrame) -> pl.DataFrame:
            prefix = "|".join(["Dr.", "Miss", "Mr.", "Mrs.", "Ms."])
            prefix_pattern = f"(^({prefix}) )"
            suffix = "|".join(["DDS", "DVM", "II", "III", "Jr.", "MD", "PhD"])
            suffix_pattern = f"( ({suffix})$)"
            strip_pattern = f"{prefix_pattern}|{suffix_pattern}"

            df = (
                df.with_columns(
                    pl.col("name")
                    .str.replace_all(strip_pattern, "")
                    .alias("processed_name"),
                )
                .with_columns(
                    pl.col("processed_name")
                    .str.split(" ")
                    .arr.get(0)
                    .alias("first_name"),
                    pl.col("processed_name")
                    .str.split(" ")
                    .arr.get(1)
                    .alias("last_name"),
                )
                .select(pl.exclude("processed_name"))
            )
            return df

        def process_date(df: pl.DataFrame) -> pl.DataFrame:
            date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y"]
            df = df.with_columns(
                pl.coalesce(
                    [
                        pl.col("date_of_birth").str.to_date(format, strict=False)
                        for format in date_formats
                    ]
                )
            ).with_columns(
                pl.col("date_of_birth").dt.strftime("%Y%m%d").alias("birthday")
            )
            return df

        def process_validity(df: pl.DataFrame) -> pl.DataFrame:
            valid_mobile_regex = "^[0-9]{8,8}$"
            valid_email_regex = "(?i:^[a-z0-9._%+-]+@[a-z0-9.-]+\.(com|net)$)"
            reference_date = datetime(2022, 1, 1)
            eighteen_years_in_days = 18 * 365

            df = df.with_columns(
                (pl.col("name").str.lengths() > 0).alias("has_valid_name"),
                pl.col("mobile_no")
                .str.contains(valid_mobile_regex)
                .alias("has_valid_mobile"),
                (
                    (pl.lit(reference_date) - pl.col("date_of_birth")).dt.days()
                    > eighteen_years_in_days
                ).alias("above_18"),
                pl.col("email")
                .str.contains(valid_email_regex)
                .alias("has_valid_email"),
            ).with_columns(
                (
                    pl.col("has_valid_name")
                    & pl.col("has_valid_mobile")
                    & pl.col("above_18")
                    & pl.col("has_valid_email")
                ).alias("is_successful")
            )
            return df

        def process_membership_id(df: pl.DataFrame) -> pl.DataFrame:
            df = df.with_columns(
                pl.concat_str(
                    pl.col("last_name"),
                    pl.col("birthday")
                    .apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
                    .str.slice(0, 5),
                    separator="_",
                ).alias("membership_id")
            )
            return df

        def process_data(df: pl.DataFrame) -> pl.DataFrame:
            df = process_date(df)
            df = process_validity(df)
            df = process_name(df)
            df = process_membership_id(df)
            return df

        def save_data(df: pl.DataFrame, save_dir: str) -> None:
            df.collect().to_pandas().to_parquet(
                save_dir,
                partition_cols=["is_successful", "ds", "ts"],
                existing_data_behavior="delete_matching",
            )

        if ts is None:
            ts = datetime(2023, 1, 1).isoformat()

        input_pattern = "input/*.csv"
        output_path = "output"

        df = load_data(input_pattern, ts)
        processed_df = process_data(df)
        save_data(processed_df, output_path)

    process_memberships_task = process_memberships()


memberships_pipeline_dag = memberships_pipeline()
