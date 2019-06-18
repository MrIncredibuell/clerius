from clericus import Clericus, Endpoint, newMethod
from clericus.parsing.fields import StringField, IntegerField


class ExampleEchoEndpoint(Endpoint):
    """
    String Echoing
    """

    async def echo(self, phrase, times):
        return {"echo": phrase * times}

    Get = newMethod(
        httpMethod="get",
        description="Echo the string given in the query",
        process=echo,
        queryParameters={
            "phrase": StringField(
                description="A string to echo some number of times"
            ),
            "times": IntegerField(
                description="The number of times to repeat the given string",
                optional=True,
                default=1,
            )
        },
        responseFields={
            "echo": StringField(),
        }
    )


server = Clericus()
server.addEndpoint("/echo/", ExampleEchoEndpoint, name="Echo Example")

server.runApp()
