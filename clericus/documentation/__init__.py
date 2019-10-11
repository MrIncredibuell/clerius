def requestDocumentationToApiBlueprint(docs):
    s = f"""
## {docs["name"]} [{docs["path"]}]

{docs["description"]}
    """

    for method, data in docs["methods"].items():
        s += f"""\n### {data["description"]} [{method.upper()}]\n"""

    print(s)

    return s
