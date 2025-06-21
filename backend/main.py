from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# import uvicorn # No longer running uvicorn from here
from pathlib import Path
import datetime
import re # For replacing comment blocks

from diagram_generator import generate_mermaid_diagram
from iac_generator import generate_iac_placeholders # Added import

app = FastAPI(
    title="Azure Data Architecture Generator API",
    description="API for generating Azure data architectures based on user requirements.",
    version="0.1.0",
)

class ArchitectureRequest(BaseModel):
    project_name: str
    use_case_description: str
    data_sources: List[str] = ["Generic CSV Files", "Operational Databases"] # Example default
    primary_processing_type: str = "Batch"
    analytical_tools_needed: List[str] = ["Dashboards", "Ad-hoc SQL"]

def replace_placeholder_block(template_content: str, placeholder_name: str, replacement_content: str) -> str:
    """Helper function to replace content between start and end comment placeholders."""
    start_comment = f"<!-- {placeholder_name}_START -->"
    end_comment = f"<!-- {placeholder_name}_END -->"
    pattern = re.compile(f"{re.escape(start_comment)}.*?{re.escape(end_comment)}", re.DOTALL)
    # Ensure the replacement content itself does not accidentally contain the placeholder comments
    # by adding the new content between the start and end comments of the placeholder.
    # This is safer if replacement_content might be user-generated or complex.
    # However, for this specific use case where we replace the *entire block including comments*,
    # the original simpler sub is fine.
    # For more controlled injection *inside* a placeholder block, one might do:
    # return pattern.sub(f"{start_comment}\n{replacement_content}\n{end_comment}", template_content)
    return pattern.sub(replacement_content, template_content)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Azure Data Architecture Generator API"}

@app.post("/generate_architecture/")
async def generate_architecture_endpoint(request: ArchitectureRequest):
    template_path = Path(__file__).parent.parent / "docs" / "architecture_output_template.md"

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Architecture template file not found.")

    # 1. Populate overview details
    populated_markdown = template_content.replace("[Project Name]", request.project_name)
    populated_markdown = populated_markdown.replace("[Use Case / Business Goals Summary]", request.use_case_description)
    populated_markdown = populated_markdown.replace("[Date]", datetime.date.today().isoformat())

    # 2. Define Markdown for predefined services (hardcoded for now)
    ingestion_services_md = """
### 2.1. Data Ingestion
| Service Name          | Role in Architecture                               | Key Configuration Notes                                       | Justification                                         |
| --------------------- | -------------------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------- |
| Azure Data Factory    | Orchestrating batch data ingestion and ETL pipelines. | Define Linked Services for sources/sinks, create pipelines. | Broad connectivity, scalable, visual interface.       |
"""
    storage_services_md = """
### 2.2. Data Storage
| Service Name                  | Role in Architecture                                  | Key Configuration Notes                                            | Justification                                                    |
| ----------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Azure Data Lake Storage Gen2  | Storing raw, semi-structured, and structured data.    | Enable hierarchical namespace, set up access tiers (hot/cool).   | Highly scalable, cost-effective, Hadoop compatible file system. |
"""
    processing_services_md = """
### 2.3. Data Processing & Transformation
| Service Name      | Role in Architecture                                      | Key Configuration Notes                                           | Justification                                                           |
| ----------------- | --------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Azure Databricks  | Large-scale data processing, transformation, and ML.      | Choose appropriate cluster sizes, use notebooks for Spark jobs.   | Powerful Spark engine, collaborative environment, ML capabilities.      |
"""
    analytical_serving_md = """
### 2.4. Analytical Data Serving / Data Warehousing
| Service Name                               | Role in Architecture                                    | Key Configuration Notes                                                 | Justification                                                                 |
| ------------------------------------------ | ------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Azure Synapse Analytics (Dedicated SQL Pool) | Serving structured data for BI and ad-hoc querying.     | Choose appropriate DWU (Data Warehouse Units), design table structures. | MPP architecture for high performance, integrates with other Azure services. |
"""
    visualization_services_md = """
### 2.5. Visualization & Reporting
| Service Name | Role in Architecture                                  | Key Configuration Notes                                       | Justification                                                              |
| ------------ | ----------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Power BI     | Creating interactive dashboards and reports.          | Connect to Azure Synapse, build data models and visuals.      | Rich visualizations, ease of use, strong integration with Azure.           |
"""

    populated_markdown = replace_placeholder_block(populated_markdown, "INGESTION_SERVICES_TABLE", ingestion_services_md)
    populated_markdown = replace_placeholder_block(populated_markdown, "STORAGE_SERVICES_TABLE", storage_services_md)
    populated_markdown = replace_placeholder_block(populated_markdown, "PROCESSING_SERVICES_TABLE", processing_services_md)
    populated_markdown = replace_placeholder_block(populated_markdown, "ANALYTICAL_SERVING_SERVICES_TABLE", analytical_serving_md)
    populated_markdown = replace_placeholder_block(populated_markdown, "VISUALIZATION_SERVICES_TABLE", visualization_services_md)

    # 4. Define services and relationships for the diagram (and IaC)
    data_sources_name = f"Data Sources ({', '.join(request.data_sources)})" if request.data_sources else 'Data Sources (Generic)'
    # This 'defined_services' list will also be used for IaC generation
    defined_services = [
        {'id': 'datasources', 'name': data_sources_name},
        {'id': 'adf', 'name': 'Azure Data Factory'},
        {'id': 'adls', 'name': 'Azure Data Lake Storage Gen2'},
        {'id': 'dbx', 'name': 'Azure Databricks'},
        {'id': 'syn', 'name': 'Azure Synapse Analytics (Dedicated SQL Pool)'},
        {'id': 'pbi', 'name': 'Power BI'}
    ]
    defined_relationships = [
        {'source_id': 'datasources', 'target_id': 'adf'},
        {'source_id': 'adf', 'target_id': 'adls'},
        {'source_id': 'adls', 'target_id': 'dbx'},
        {'source_id': 'dbx', 'target_id': 'syn'},
        {'source_id': 'syn', 'target_id': 'pbi'}
    ]

    # Generate Mermaid diagram code
    mermaid_code = generate_mermaid_diagram(defined_services, defined_relationships)
    populated_markdown = replace_placeholder_block(populated_markdown, "MERMAID_DIAGRAM", mermaid_code)

    # 5. Generate IaC placeholder suggestions
    # We pass defined_services, but filter out 'datasources' as it's not an Azure resource to provision.
    azure_services_for_iac = [s for s in defined_services if s['id'] != 'datasources']
    iac_suggestions_markdown = generate_iac_placeholders(azure_services_for_iac)
    populated_markdown = replace_placeholder_block(populated_markdown, "IAC_SUGGESTIONS", iac_suggestions_markdown)

    return {"architecture_markdown": populated_markdown}

if __name__ == "__main__":
    # This block is now commented out to prevent conflicts when running uvicorn directly from CLI
    # import uvicorn
    # uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
    pass
