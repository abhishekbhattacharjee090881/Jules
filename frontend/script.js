document.getElementById('architectureForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const resultsArea = document.getElementById('resultsArea');
    resultsArea.innerHTML = '<p>Generating architecture... Please wait.</p>';

    const formData = new FormData(this);
    const data = {
        project_name: formData.get('project_name'),
        use_case_description: formData.get('use_case_description'),
        data_sources: formData.get('data_sources').split(',').map(s => s.trim()).filter(s => s),
        primary_processing_type: formData.get('primary_processing_type'),
        analytical_tools_needed: []
    };
    formData.getAll('analytical_tools').forEach(tool => {
        data.analytical_tools_needed.push(tool);
    });

    console.log('Request Payload:', data);

    try {
        // SIMULATED BACKEND RESPONSE:
        await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay

        // New tailored markdown for "E-commerce Sales Reporting Data Mart"
        const architecture_markdown = `
# Azure Data Architecture Proposal: ${data.project_name}
## Date: ${new Date().toLocaleDateString()}

## 1. Overview
This architecture outlines an **E-commerce Sales Data Mart** designed for your project: *${data.use_case_description}*.
It will process data primarily from sources like *${data.data_sources.join(', ') || 'OrderDB, WebLogs'}* using a **${data.primary_processing_type}** approach.
The core objective is to build a relational star schema for efficient sales and customer behavior reporting.

## 2. Proposed Azure Services

### 2.1 Data Ingestion & Transformation Orchestration
*   **Azure Data Factory (ADF)**
    *   **Role:** Orchestrate data extraction from sources (e.g., OrderDB, WebLogs via Blob), stage data in ADLS Gen2, execute data transformation logic (e.g., using Mapping Data Flows or invoking other processes), and load the final star schema into Azure SQL Database.
    *   **Key Configuration Notes:** Define linked services for all sources and sinks; develop pipelines for daily batch loads; implement robust error handling and logging.
    *   **Justification:** Provides a comprehensive, serverless platform for ETL/ELT orchestration with broad connectivity.

### 2.2 Staging & Intermediate Storage
*   **Azure Data Lake Storage (ADLS) Gen2**
    *   **Role:** Store raw copies of source data (e.g., daily OrderDB extracts, weblog files) and serve as a staging area for intermediate data during transformation processes.
    *   **Key Configuration Notes:** Organize with clear folder structures (e.g., /raw/OrderDB/, /raw/WebLogs/, /processed/DimProduct/, /processed/FactSales/).
    *   **Justification:** Cost-effective, scalable storage for large volumes of diverse data types, optimized for analytical workloads.

### 2.3 Relational Data Mart Storage
*   **Azure SQL Database**
    *   **Role:** Host the final, structured Sales Data Mart, designed as a star schema (e.g., DimProduct, DimCustomer, DimDate, FactSales).
    *   **Key Configuration Notes:** Choose an appropriate service tier (DTU/vCore based); implement indexing for query performance; secure access.
    *   **Justification:** Provides a managed, relational database service well-suited for serving structured data to Power BI and for ad-hoc analytical queries.

### 2.4 Visualization & Reporting
*   **Microsoft Power BI**
    *   **Role:** Develop interactive dashboards and reports for sales trends, customer segmentation, product performance, etc., based on data in the Azure SQL Data Mart.
    *   **Key Configuration Notes:** Connect to Azure SQL Database using Import or DirectQuery mode; design effective data models and visuals.
    *   **Justification:** Powerful business analytics tool with strong integration with Azure data services.

## 3. Architecture Diagram (Mermaid.js)
<!-- MERMAID_DIAGRAM_START -->
\`\`\`mermaid
graph TD
    DS["Data Sources (${data.data_sources.join('\\n') || 'OrderDB, WebLogs'})" ] --> ADF[Azure Data Factory];
    ADF -- "Extract & Stage" --> ADLS{Azure Data Lake Storage Gen2 (Staging)};
    ADLS -- "Read for Transformation" --> ADF;
    ADF -- "Load Star Schema" --> SQLMART[(Azure SQL Database - Sales Data Mart)];
    SQLMART --> PBI(Power BI Reports);
\`\`\`
<!-- MERMAID_DIAGRAM_END -->

## 4. High-Level Setup Steps
1.  **Provision Azure Resources:** Create instances of Azure Data Factory, Azure Data Lake Storage Gen2, and Azure SQL Database in your chosen region.
2.  **Configure Storage:** Set up containers and folder structures in ADLS Gen2. Design the star schema (tables, relationships, indexes) in Azure SQL Database.
3.  **Develop ADF Pipelines:**
    a.  Create pipelines to extract data from source systems (e.g., OrderDB, WebLogs) into ADLS Gen2.
    b.  Develop data transformation logic (e.g., using Mapping Data Flows) to cleanse, join, aggregate data, and create dimension and fact entities.
    c.  Create pipelines to load the transformed data from ADLS Gen2 into the Azure SQL Data Mart tables.
4.  **Schedule Pipelines:** Configure triggers for daily execution of the ADF pipelines.
5.  **Develop Power BI Reports:** Connect Power BI to the Azure SQL Data Mart. Build data models and create interactive reports and dashboards.
6.  **Implement Security & Monitoring:** Secure access to all services and set up monitoring and logging.

## 5. Infrastructure as Code (IaC) Suggestions (Placeholders)
<!-- IAC_SUGGESTIONS_START -->
Conceptual IaC placeholders for Azure Data Factory, ADLS Gen2, Azure SQL Database would be detailed here. For example:

### Azure SQL Database
\`\`\`json
{
  "resourceType": "Microsoft.Sql/servers/databases",
  "name": "[concat(parameters('sqlServerName'), '/', parameters('sqlDatabaseName'))]",
  "apiVersion": "2022-08-01-preview",
  "location": "[parameters('location')]",
  "sku": {
    "name": "GP_Gen5",
    "tier": "GeneralPurpose",
    "capacity": 2
  },
  "properties": {
    "collation": "SQL_Latin1_General_CP1_CI_AS",
    "sampleName": "AdventureWorksLT"
  }
}
\`\`\`
<!-- IAC_SUGGESTIONS_END -->

## 6. Next Steps & Considerations
-   Perform detailed data modeling for the star schema.
-   Focus on data quality and validation throughout the ETL process.
-   Optimize ADF pipeline performance and Azure SQL Database configurations.
-   Implement robust security measures and data governance practices.
`;

        const simulatedBackendResult = { architecture_markdown };
        const markdownContent = simulatedBackendResult.architecture_markdown;
        // End of SIMULATED BACKEND RESPONSE

        if (typeof marked !== 'undefined') {
            resultsArea.innerHTML = marked.parse(markdownContent);
        } else {
            resultsArea.innerHTML = "Error: marked.js library not loaded.";
            return;
        }

        if (typeof mermaid !== 'undefined') {
            const mermaidDiagrams = resultsArea.querySelectorAll('.mermaid');
            if (mermaidDiagrams.length > 0) {
                mermaid.run({ nodes: mermaidDiagrams });
            } else {
                // Fallback to find pre > code blocks for mermaid
                const preElements = resultsArea.querySelectorAll('pre');
                preElements.forEach(pre => {
                    const code = pre.querySelector('code');
                    // A simple check if it looks like a mermaid definition
                    if (code && (code.textContent.includes('graph TD') || code.textContent.includes('graph LR'))) {
                        const mermaidContainer = document.createElement('div');
                        mermaidContainer.classList.add('mermaid');
                        mermaidContainer.textContent = code.textContent;
                        pre.parentNode.replaceChild(mermaidContainer, pre);
                    }
                });
                mermaid.run({ nodes: resultsArea.querySelectorAll('.mermaid') });
            }
        } else {
            console.warn("Mermaid library not loaded. Diagrams will not be rendered.");
        }

    } catch (error) {
        console.error('Error generating architecture:', error);
        resultsArea.innerHTML = `<p>Error: Could not generate architecture. ${error.message}</p>`;
    }
});
