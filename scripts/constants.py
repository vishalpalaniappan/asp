ASV_DEF = {
    "CONTAINER_NAME": "asv-container",
    "IMAGE_NAME": "asv-image",
    "IMAGE_PATH": "docker-images/asv/Dockerfile",
    "COMPONENT_PATH": "components_new/asv",
    "PORT": 3012,
    "DATA_DIR": "data/asv",
}

DLV_DEF = {
    "CONTAINER_NAME": "dlv-container",
    "IMAGE_NAME": "dlv-image",
    "IMAGE_PATH": "docker-images/dlv/Dockerfile",
    "COMPONENT_PATH": "components_new/dlv",
    "PORT": 3011,
    "DATA_DIR": "data/dlv",
}

DB_DEF = {
    "CONTAINER_NAME": "mariadb-container",
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

NET_DEF = {
    "NETWORK_NAME": "asp-network"
}


