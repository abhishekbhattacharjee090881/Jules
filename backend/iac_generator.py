from typing import List, Dict, Any

def generate_iac_placeholders(services: List[Dict[str, Any]]) -> str:
    """
    Generates placeholder IaC snippets for a list of services.
    """
    if not services:
        return "\n## Infrastructure as Code (IaC) Suggestions\n\nNo services selected for IaC generation."

    iac_snippets = ["\n## 5. Infrastructure as Code (IaC) Suggestions (Placeholders)\n"] # Matched section number
    iac_snippets.append("Below are conceptual placeholders for IaC. Full IaC generation is a complex feature requiring detailed specifications and choices (e.g., ARM, Bicep, Terraform).\n")

    for service in services:
        service_name = service.get('name', 'Unnamed Service')
        service_id = service.get('id', 'unknown_id')

        # Sanitize service_name for resourceType by removing spaces and special chars, ensure it's valid
        sanitized_service_name_for_type = ''.join(filter(str.isalnum, service_name))
        if not sanitized_service_name_for_type:
            sanitized_service_name_for_type = "GenericService"


        iac_snippets.append("\n### " + service_name + " (ID: " + service_id + ")\n")
        iac_snippets.append("```json")
        iac_snippets.append("{")
        iac_snippets.append("  \"$schema\": \"https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#\",")
        iac_snippets.append("  \"contentVersion\": \"1.0.0.0\",")
        iac_snippets.append("  \"parameters\": {")
        iac_snippets.append("    \"" + service_id + "_name\": {")
        iac_snippets.append("      \"type\": \"string\",")
        iac_snippets.append("      \"defaultValue\": \"" + service_id + "-default-name\",")
        iac_snippets.append("      \"metadata\": {")
        iac_snippets.append("        \"description\": \"Name for the " + service_name + "\"")
        iac_snippets.append("      }")
        iac_snippets.append("    },")
        iac_snippets.append("    \"location\": {")
        iac_snippets.append("      \"type\": \"string\",")
        iac_snippets.append("      \"defaultValue\": \"[resourceGroup().location]\",")
        iac_snippets.append("      \"metadata\": {")
        iac_snippets.append("        \"description\": \"Location for all resources.\"")
        iac_snippets.append("      }")
        iac_snippets.append("    }")
        iac_snippets.append("  },")
        iac_snippets.append("  \"resources\": [")
        iac_snippets.append("    {")
        iac_snippets.append("      \"type\": \"Microsoft.Placeholder/" + sanitized_service_name_for_type + "\",") # Use sanitized name
        iac_snippets.append("      \"apiVersion\": \"2023-01-01-preview\",") # Example API version
        iac_snippets.append("      \"name\": \"[parameters('" + service_id + "_name')]\",")
        iac_snippets.append("      \"location\": \"[parameters('location')]\",")
        iac_snippets.append("      \"properties\": {")
        iac_snippets.append("        \"displayName\": \"" + service_name + "\",")
        iac_snippets.append("        \"description\": \"Placeholder for IaC for " + service_name + " - further details needed\"")
        iac_snippets.append("      }")
        iac_snippets.append("    }")
        iac_snippets.append("  ]")
        iac_snippets.append("}")
        iac_snippets.append("```")
        iac_snippets.append("\n*Note: This is a conceptual ARM template placeholder. Actual resource types and properties will vary significantly.*")
        iac_snippets.append("\n// TODO: Define detailed ARM/Bicep/Terraform template for " + service_name + "\n")

    return "\n".join(iac_snippets)

if __name__ == '__main__':
    example_services = [
        {'id': 'adf', 'name': 'Azure Data Factory'},
        {'id': 'adls', 'name': 'Azure Data Lake Storage Gen2'},
        {'id': 'dbx', 'name': 'Azure Databricks'}
    ]
    iac_output = generate_iac_placeholders(example_services)
    print("Generated IaC Placeholders for testing:")
    print(iac_output)
