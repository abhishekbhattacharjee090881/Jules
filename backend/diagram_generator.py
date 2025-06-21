from typing import List, Dict, Any

def generate_mermaid_diagram(services: List[Dict[str, Any]], relationships: List[Dict[str, str]]) -> str:
    """
    Generates a Mermaid.js diagram string from a list of services and their relationships.
    Args:
        services: List of service dicts, e.g., [{'id': 's1', 'name': 'Service1'}, ...].
        relationships: List of relationship dicts, e.g., [{'source_id': 's1', 'target_id': 's2'}, ...].
    Returns:
        String containing Mermaid.js diagram syntax.
    """
    if not services:
        return "```mermaid\ngraph TD\n    A[No services defined];\n```"

    mermaid_lines = ["```mermaid", "graph TD;"]

    for service in services:
        node_id = service['id']
        # Replace quotes in names to avoid breaking Mermaid syntax
        node_name = service['name'].replace('"', '#quot;')
        mermaid_lines.append(f"    {node_id}[\"{node_name}\"];") # Node name in quotes

    for rel in relationships:
        mermaid_lines.append(f"    {rel['source_id']} --> {rel['target_id']};")

    mermaid_lines.append("```")
    return "\n".join(mermaid_lines)

if __name__ == '__main__':
    example_services = [
        {'id': 'ds', 'name': 'Data Sources (CSV, DB)'},
        {'id': 'adf', 'name': 'Azure Data Factory'},
        {'id': 'adls', 'name': 'Azure Data Lake Storage Gen2'},
        {'id': 'dbx', 'name': 'Azure Databricks'},
        {'id': 'syn', 'name': 'Azure Synapse Analytics'},
        {'id': 'pbi', 'name': 'Power BI'}
    ]
    example_relationships = [
        {'source_id': 'ds', 'target_id': 'adf'},
        {'source_id': 'adf', 'target_id': 'adls'},
        {'source_id': 'adls', 'target_id': 'dbx'},
        {'source_id': 'dbx', 'target_id': 'syn'},
        {'source_id': 'syn', 'target_id': 'pbi'}
    ]
    diagram_code = generate_mermaid_diagram(example_services, example_relationships)
    print("Generated Mermaid Code for testing:")
    print(diagram_code)
