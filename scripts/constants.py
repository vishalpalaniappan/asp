ASV_DEF = {
    "CONTAINER_NAME": "asp-asv-container",
    "IMAGE_NAME": "asp-asv-image",
    "IMAGE_PATH": "docker-images/asv/Dockerfile",
    "COMPONENT_PATH": "components_new/asv",
    "PORT": 3012,
    "DATA_DIR": "data/asv",
}

DLV_DEF = {
    "CONTAINER_NAME": "asp-dlv-container",
    "IMAGE_NAME": "asp-dlv-image",
    "IMAGE_PATH": "docker-images/dlv/Dockerfile",
    "COMPONENT_PATH": "components_new/dlv",
    "PORT": 3011,
    "DATA_DIR": "data/dlv",
}

DB_DEF = {
    "CONTAINER_NAME": "asp-mariadb-container",
    "PORT": 3306,
    "DATABASE_NAME": "aspDatabase",
    "DATABASE_PASSWORD": "random-password",
    "DATA_DIR": "data/mariadb",
}

ASP_DEF = {
    "CONTAINER_NAME": "asp-container",
    "IMAGE_NAME": "asp-image",
    "IMAGE_PATH": "docker-images/asp/Dockerfile",
    "COMPONENT_PATH": "components_new/asp",
    "DATA_DIR": "data/asp",
}

QUERY_HANDLER_DEF = {
    "CONTAINER_NAME": "query-handler-container",
    "PORT": 8765,
    "IMAGE_NAME": "query-handler-image",
    "IMAGE_PATH": "docker-images/query_handler/Dockerfile",
    "COMPONENT_PATH": "components_new/query_handler",
    "DATA_DIR": "data/query_handler",
}

NET_DEF = {
    "NETWORK_NAME": "asp-network"
}


