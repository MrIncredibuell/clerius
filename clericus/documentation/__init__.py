def requestDocumentationToApiBlueprint(docs):
    queryParameters = []
    for method in docs.get("methods", {}).values():
        queryParameters += method.get(
            "requestParameters",
            {},
        ).get(
            "query",
            {},
        ).keys()

    queryParameterString = ",".join(sorted(set(queryParameters)))

    if queryParameters:
        queryParameters = "{?" + queryParameterString + "}"

    s = f"""
## {docs["name"]} [{docs["path"]}{queryParameters}]

{docs["description"]}
    """

    for method, data in docs["methods"].items():
        s += f"""\n### {data["description"]} [{method.upper()}]\n"""

        parameters = data.get(
            "requestParameters",
            {},
        )

        displayableParameters = sorted(
            list(parameters.get(
                "url",
                {},
            ).items()) + list(parameters.get(
                "query",
                {},
            ).items())
        )

        if displayableParameters:
            s += "\n+ Parameters\n"

            for name, parameter in displayableParameters:
                allowedTypes = parameter.get("allowedTypes", [])
                if len(allowedTypes) == 1:
                    allowedTypes = allowedTypes[0]
                elif allowedTypes:
                    allowedTypes = ",".join(allowedTypes)
                else:
                    allowedTypes = "any"

                optional = "optional" if parameter.get(
                    "optional"
                ) else "required"

                description = parameter.get("description")

                default = parameter.get("default")
                s += f"\n\t+ {name} ({allowedTypes}, {optional}) - {description}\n"
                if default is not None:
                    s += f"\t\t+ Default: `{default}`\n`"

    print(s)

    return s
