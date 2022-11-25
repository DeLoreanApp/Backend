from dotenv import load_dotenv

load_dotenv()
from os import environ
from .db import engine, Base
from .routers import *
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

metadata_tags = [
    {
        "name": "WIP",
        "description": "This methods are under development and most likely will be changed",
    },
]

app = FastAPI(
    title="DeLorian",
    openapi_tags=metadata_tags,
    swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
)

app.include_router(users)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    routes = []
    for route in app.routes:
        if tags := getattr(route, "tags", None):
            if "WIP" in tags:
                continue
        routes.append(route)

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="DeLorian api unstable docs",
        routes=routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


if environ.get("STABLE_DOCS"):
    app.openapi = custom_openapi
