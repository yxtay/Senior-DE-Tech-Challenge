# Senior Data Enginer Tech Challenge
---
## Section2: Databases

You are the tech lead for an e-commerce company that operates on the cloud. The company allows users to sign up as members on their website and make puchases on items listed. You are required to design and implement a pipeline that processes membership applications and determine if an application is successful or unsuccessful. Applications are dropped into a location for processing. Engineers have already written code to determine a successful or unsuccessful application, as well as creating membership IDs for successful applications. You may use the processed datasets from section 1 as reference. Successful applications should be sent to a location for storage and refrence. 

The e-commerce company also requires you to set up a database for their sales transactions. 
Set up a PostgreSQL database using the Docker [image](https://hub.docker.com/_/postgres) provided. We expect at least a Dockerfile which will stand up your database with the DDL statements to create the necessary tables.vYou are required to produce  entity-relationship diagrams as necessary to illustrate your design, along with the DDL statements that will be required to stand up the databse. 
The following are known for each item listed for sale on the e-commerce website:
- Item Name
- Manufacturer Name
- Cost
- Weight (in kg)

Each transaction made by a member contains the following information:
- Membership ID
- Items bought
- Total items price
- Total items weight

Analysts from the e-commerce company will need to query some information from the database. Below are 2 of the sameple queries from the analysts. Do note to design your database to account for a wide range of business use cases and queries. 
You are tasked to write a SQL statement for each of the following task:
1. Which are the top 10 members by spending
2. Which are the top 3 items that are frequently brought by members


---

## Section3: System Design

### Design 1
We will be referencing the database from Section2 in this design.. This database will be used by several teams within the company to track the orders of members. You are required to implement a strategy for accessing this database based on the various teams' needs. These teams include:
- Logistics: 
    - Get the sales details (in particular the weight of the total items bought)
    - Update the table for completed transactions
- Analytics:
    - Perform analysis on the sales and membership status
    - Should not be able to perform updates on any tables
- Sales:
    - Update databse with new items
    - Remove old items from database


### Design 2

You are designing data infrastructure on the cloud for a company whose main business is in processing images.

The company has a web application which allows users to upload images to the cloud using an API. There is also a separate web application which hosts a Kafka stream that uploads images to the same cloud environment. This Kafka stream has to be managed by the company's engineers. 

Code has already been written by the company's software engineers to process the images. This code has to be hosted on the cloud. For archival purposes, the images and its metadata has to be stored in the cloud environment for 7 days, after which it has to be purged from the environment for compliance and privacy. The cloud environment should also host a Business Intelligence resource where the company's analysts can access and perform analytical computation on the data stored.

As a technical lead of the company, you are required to produce a system architecture diagram (Visio, PowerPoint, draw.io) depicting the end-to-end flow of the aforementioned pipeline. You may use any of the cloud providers (e.g. AWS, Azure, GCP) to host the environment. The architecture should specifically address the requirements/concerns above. 

In addition, you will need to address several key points brought by stakeholders. These includes:
- Securing access to the environment and its resources as the company expands
- Security of data at rest and in transit
- Scaling to meet user demand while keeping costs low
- Maintainance of the environment and assets (including processing scripts)


You will need to ensure that the architecture takes into account the best practices of cloud computing. This includes (non-exhaustive):
- Managability
- Scalability
- Secure
- High Availability
- Elastic
- Fault Tolerant and Disaster Recovery
- Efficient
- Low Latency
- Least Privilege

Do indicate any assumptions you have made regarding the architecture. You are required to provide a detailed explanation on the diagram.

---
## Section 4: Charts & APIs
Your team decided to design a dashboard to display the statistic of COVID19 cases. You are tasked to display one of the components of the dashboard which is to display a visualisation representation of number of COVID19 cases in Singapore over time.

Your team decided to use the public data from https://documenter.getpostman.com/view/10808728/SzS8rjbc#b07f97ba-24f4-4ebe-ad71-97fa35f3b683.

Display a graph to show the number cases in Singapore over time using the APIs from https://covid19api.com/.

Note: please submit screenshots of the dashboard

---


## Section 5: Machine Learning
Using the dataset from https://archive.ics.uci.edu/ml/datasets/Car+Evaluation, create a machine learning model to predict the buying price given the following parameters:

Maintenance = High <br>
Number of doors = 4 <br>
Lug Boot Size = Big <br>
Safety = High <br>
Class Value = Good <br>