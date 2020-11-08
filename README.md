# Proof of Concept Portal

**Backend Stack**

```
Backend : [ Nginx HTTP proxy <-> Gunicorn * [Uvicorn ASGI] @ Python 3.7 > FastAPI -> PostgreSQL ]

    <--- HTTP JSON XHR / REST API --->

Browser > Web Frontend
```

* [FastAPI](https://fastapi.tiangolo.com) Web Framework to build REST server

 **key features:**
 - fast and competitive
 - asynchronous I/O event loop using [libuv](https://github.com/libuv/libuv)
 - support [OpenAPI](https://github.com/OAI/OpenAPI-Specification) / [JSON Schema](http://json-schema.org)
 - generate automatic interactive documentation
 - load JSON to class object and verify schema
 - support [GraphQL](https://graphql.org)

* [Starlette](https://github.com/encode/starlette) ASGI framework/toolkit
* [Uvicorn](https://www.uvicorn.org) ASGI server as [Gunicorn](https://gunicorn.org) worker
* [SqlAlchemy](https://www.sqlalchemy.org) ORM -> [PostgreSQL](https://www.postgresql.org)
* [MJML](https://mjml.io) Responsive Email Framework

# Urls

* OpenAPI : http://localtest.me:8000/docs
