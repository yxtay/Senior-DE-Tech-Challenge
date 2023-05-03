# Senior Data Enginer Tech Challenge
---
## Section1: Data Pipelines
An e-commerce company requires that users sign up for a membership on the website in order to purchase a product from the platform. As a data engineer under this company, you are tasked with designing and implementing a pipeline to process the membership applications submitted by users on an hourly interval.

Applications are batched into a varying number of datasets and dropped into a folder on an hourly basis. You are required to set up a pipeline to ingest, clean, perform validity checks, and create membership IDs for successful applications. An application is successful if:

- Application mobile number is 8 digits
- Applicant is over 18 years old as of 1 Jan 2022
- Applicant has a valid email (email ends with @emailprovider.com or @emailprovider.net)

You are required to format datasets in the following manner:

- Split name into first_name and last_name
- Format birthday field into YYYYMMDD
- Remove any rows which do not have a name field (treat this as unsuccessful applications)
- Create a new field named above_18 based on the applicant's birthday
- Membership IDs for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)

You are required to consolidate these datasets and output the successful applications into a folder, which will be picked up by downstream engineers. Unsuccessful applications should be condolidated and dropped into a separate folder.

You can use common scheduling solutions such as cron or airflow to implement the scheduling component. Please provide a markdown file as documentation.

Note: Please submit the processed dataset and scripts used

### Instructions

Set up airflow
```
docker compose up --build -d
```

Execute a DAG
```
docker compose exec airflow-worker airflow dags test memberships_pipeline 2023-01-01
```

The data pipeline is defined as a DAG in airflow. You may find it in the [dags](dags/memberships_dag.py) folder.

Processed data is saved in `output` folder. 
Successful applications in `output/is_succssful=true`, failed applications in `output/is_succssful=false`.

Usually, the data should have a suitable datetime partition or in the path name to allow idempotent behaviour.
In this task, my pipeline is always reading from the same data source to simulate the data being available.
I have added the ds and ts columns into the data as part of the pipeline to simulate the data partitions.

In general, I would have preferred to run the task in an environment isolated from airflow, 
such as using virtual environment, DockerOperator or KubernetesOperator.
However, given the time constraint, I have opted to provide a minimum workable solution here sharing environment with airflow.

### Clean up

```
docker compose down --volumes --remove-orphans --rmi all
```
