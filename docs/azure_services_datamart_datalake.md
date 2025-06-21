# Key Azure Services for Modern Data Warehouse/Data Lake

This list will serve as a reference for the application's backend logic when designing Azure data solutions.

**1. Data Ingestion:**
    - **Azure Data Factory (ADF):** Orchestrates batch ETL/ELT from diverse sources. Code-free UI, numerous connectors.
    - **Azure Event Hubs:** High-throughput ingestion for real-time event streams (e.g., logs, IoT telemetry).
    - **Azure IoT Hub:** Manages and ingests data from IoT devices, with bi-directional communication.
    - **Azure Synapse Link:** Near real-time analytics over operational data in Azure Cosmos DB, Azure SQL Database, etc., without impacting source systems.

**2. Data Storage:**
    - **Azure Data Lake Storage (ADLS) Gen2:** Scalable, secure data lake solution for structured, semi-structured, and unstructured data. Built on Azure Blob Storage with hierarchical namespace.
    - **Azure Blob Storage:** General-purpose object storage for various data types, backups, archives.

**3. Data Processing & Transformation:**
    - **Azure Databricks:** Apache Spark-based platform for large-scale data engineering, ETL, and machine learning. Supports Python, Scala, SQL, R.
    - **Azure Synapse Analytics:**
        - **Spark Pools:** Managed Spark for big data processing within Synapse.
        - **Data Integration (Pipelines):** ADF-like capabilities for orchestration within Synapse.
    - **Azure Data Factory (Mapping Data Flows):** Visual, code-free data transformation running on managed Spark clusters.
    - **Azure Stream Analytics:** Real-time event processing for streaming data, with SQL-like query language.

**4. Analytical Data Serving / Data Warehousing:**
    - **Azure Synapse Analytics:**
        - **Dedicated SQL Pools:** MPP-based enterprise data warehousing for serving processed data.
        - **Serverless SQL Pools:** Ad-hoc T-SQL querying directly on data in ADLS Gen2 or Cosmos DB.
    - **Azure Analysis Services / Power BI Premium Datasets:** Semantic modeling layer for high-performance BI and interactive querying.

**5. Visualization & Reporting:**
    - **Microsoft Power BI:** Interactive dashboards, reports, and business analytics tools. Connects to a wide array of data sources.

**6. Security & Governance (Cross-Cutting):**
    - **Azure Active Directory (Azure AD):** Identity and access management.
    - **Azure Key Vault:** Secrets management.
    - **Azure Monitor & Log Analytics:** Performance and application monitoring.
    - **Microsoft Purview:** Unified data governance (discovery, classification, lineage).
