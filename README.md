# Clericus

Clericus is an asynchronous webserver (wrapping aiohttp) which tries to abstract away the boring parts of writing a webserver by making parsing request, serializing data, and generating documentation build in.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Clericus requires Python 3.7.

### Installing

Clericus is on pypi, but is still in alpha, so your mileage may vary.  Install the latest alpha release (which is probably a different version by now) like so:

```
pip install clericus==0.0.3a4
```

## Running the tests

Tests are built with unittest and can be run via:

```
python -m unittest 
```

Add the `-v` flag if you want more verbosity.


## Usage

The following code sets up and runs a simple webserver:

```python
from clericus import Clericus, Endpoint, newMethod
from clericus.parsing.fields import StringField, IntegerField


class ExampleEchoEndpoint(Endpoint):
    """
    String Echoing
    """

    async def echo(self, phrase, times):
        return {"echo": phrase * times}

    Get = newMethod(
        httpMethod="GET",
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
```

With the webserver running, in another tab do:

```
$ (master)$ curl 'localhost:8080/echo/?phrase=hello-world&times=3'
{"echo": "hello-worldhello-worldhello-world"}
```

Because the `times` parameter is optional, it can be omitted and the configured default will be used.

```
$ (master)$ curl 'localhost:8080/echo/?phrase=hello-world'
{"echo": "hello-world"}
```

Leaving out the required `phrase` parameter will cause the server to response with an automatically generated error:

```
$ (master)$ curl 'localhost:8080/echo/'
{"errors": [{"message": "Missing required field: phrase"}]}
```

Clericus also handles documentation based on your configuration, so any endpoint you add also adds another `documentation` endpoint like so (JSON expanded for clarity):

```
$curl 'localhost:8080/documentation/echo/'
{
    "description": "String Echoing",
    "name": "Echo Example",
    "path": "/echo/",
    "methods": {
        "get": {
            "description": "Echo the string given in the query",
            "request": {
                "query": {
                    "phrase": {
                        "allowedTypes": [
                            "string"
                        ],
                        "optional": false,
                        "default": null,
                        "description": "A string to echo some number of times"
                    },
                    "times": {
                        "allowedTypes": [
                            "int"
                        ],
                        "optional": true,
                        "default": 1,
                        "description": "The number of times to repeat the given string"
                    }
                }
            },
            "response": {
                "body": {
                    "echo": {
                        "allowedTypes": [
                            "string"
                        ],
                        "optional": false,
                        "default": null,
                        "description": ""
                    }
                }
            }
        },
        "options": {
            "description": null,
            "request": {},
            "response": {
                "body": {}
            }
        }
    }
}
```


Clericus also assumes the root path should be the documentation for your API, so you can do the following to see all endpoints (currently some authentication methods are always included, I plan to factor these out later...)

```
curl 'localhost:8080/'
{
    "endpoints": [
        {
            "description": "String Echoing",
            "name": "Echo Example",
            "path": "/echo/",
            "methods": {
                "get": {
                    "description": "Echo the string given in the query",
                    "request": {
                        "query": {
                            "phrase": {
                                "allowedTypes": [
                                    "string"
                                ],
                                "optional": false,
                                "default": null,
                                "description": "A string to echo some number of times"
                            },
                            "times": {
                                "allowedTypes": [
                                    "int"
                                ],
                                "optional": true,
                                "default": 1,
                                "description": "The number of times to repeat the given string"
                            }
                        }
                    },
                    "response": {
                        "body": {
                            "echo": {
                                "allowedTypes": [
                                    "string"
                                ],
                                "optional": false,
                                "default": null,
                                "description": ""
                            }
                        }
                    }
                },
                "options": {
                    "description": null,
                    "request": {},
                    "response": {
                        "body": {}
                    }
                }
            }
        },
        {
            "description": "Return the status of the server",
            "path": "/healthy/",
            "methods": {
                "get": {
                    "description": "Return the status of the server",
                    "request": {},
                    "response": {
                        "body": {
                            "healthy": {
                                "allowedTypes": [],
                                "optional": false,
                                "default": true,
                                "description": "A boolean of whether the server is healthy"
                            }
                        }
                    }
                },
                "options": {
                    "description": null,
                    "request": {},
                    "response": {
                        "body": {}
                    }
                }
            }
        },
        ...
    ]
}
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/MrIncredibuell/clerius/tags). 

## Authors

* **Joseph Buell** - *Initial work* - [MrIncredibuell](https://github.com/MrIncredibuell)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


