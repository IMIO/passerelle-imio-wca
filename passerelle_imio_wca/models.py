import json

import requests
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint


class ConnectorWCA(BaseResource):
    """
    Connector WCA
    """
    api_description = "Connecteur permettant d'intéragir avec la plateforme WCA"
    category = "Connecteurs iMio"

    class Meta:
        verbose_name = "Connecteur pour WCA"

    username = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Username",
        help_text="Username pour la connexion à WCA",
    )

    password = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Mot de passe",
        help_text="Mot de passe pour la connexion à WCA",
    )

    url_authentic = models.URLField(
        verbose_name="URL authentic",
        help_text="URL de de base de connexion à authentic\nExemple https://agents.wallonie-connect.be/",
        default="https://agents.wallonie-connect.be/"
    )

    username_imio = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Username iMio",
        help_text="Username pour la connexion My iMio",
    )

    password_imio = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Mot de passe iMio",
        help_text="Mot de passe pour la connexion à My iMio",
    )

    url_authentic_imio = models.URLField(
        verbose_name="URL authentic iMio",
        help_text="URL de de base de connexion à authentic My iMio",
        default="https://my.imio.be/"
    )


    @endpoint(
        name="user",
        perm="can_access",
        methods=["get"],
        description="Get users",
        long_description="Permet de chercher des utilisateurs dans WCA",
        display_order=0,
        display_category="USERS",
        pattern="^get",
        example_pattern="get",
        parameters={
            "email__iexact": {
                "description": "email du user",
                "example_value": "admints@imio.be",
            },
        },
    )
    def get_user(self, request, email__iexact=None):
        username = self.username
        password = self.password
        url = f"{self.url_authentic}api/users/"

        if email__iexact:
            url += f"?email__iexact={email__iexact}"
            # url += "&".join(f"{key}={value}" for key, value in {"email__iexact": email__iexact} if value)

        headers = {"Content-Type": "application/json"}
        auth = (username, password)

        response = requests.get(url=url, headers=headers, auth=auth)
        response.raise_for_status()

        return response.json()

    @endpoint(
        name="user",
        perm="can_access",
        methods=["post"],
        description="Create user",
        long_description="Permet de créer des utilisateurs dans WCA",
        display_order=1,
        display_category="USERS",
        pattern="^create",
        example_pattern="create"
    )
    def post_user(self, request):
        username = self.username
        password = self.password
        url = f"{self.url_authentic}api/users/?update_or_create=email"

        headers = {"Content-Type": "application/json"}
        auth = (username, password)
        data = request.body

        response = requests.post(url=url, headers=headers, auth=auth, data=data)
        response.raise_for_status()

        return response.json()


    @endpoint(
        name="roles",
        perm="can_access",
        methods=["get"],
        description="Get roles",
        long_description="Permet d'obtenir la liste des rôles dans WCA",
        display_category="ROLES",
    )
    def get_roles(self, request):
        username = self.username
        password = self.password
        url = f"{self.url_authentic}api/roles/?limit=100000"

        auth = (username, password)

        response = requests.get(url=url, auth=auth)

        response.raise_for_status()

        return response.json()

    @endpoint(
        name="roles",
        perm="can_access",
        methods=["post"],
        description="Add role to a user",
        long_description="Permet d'ajouter un utilisateur dans un rôle",
        display_category="ROLES",
        pattern="^add_user",
        example_pattern="add_user"
    )
    def add_role_user(self, request):
        username = self.username
        password = self.password

        post_data = json.loads(request.body)
        self.logger.info(post_data)
        role_uuid = post_data["role_uuid"]
        user_uuid = post_data["user_uuid"]

        url = f"{self.url_authentic}api/roles/{role_uuid}/members/{user_uuid}/"
        self.logger.info(url)
        auth = (username, password)

        response = requests.post(url=url, auth=auth)

        response.raise_for_status()

        return response.json()

        @endpoint(
        name="roles",
        perm="can_access",
        methods=["post"],
        description="Add role to a user",
        long_description="Permet d'ajouter un utilisateur dans un rôle sur My iMio",
        display_category="ROLES",
        pattern="^add_user",
        example_pattern="add_user"
    )
    def add_role_user_imio(self, request):
        username = self.username_imio
        password = self.password_imio

        post_data = json.loads(request.body)
        self.logger.info(post_data)
        role_uuid = post_data["role_uuid"]
        user_uuid = post_data["user_uuid"]

        url = f"{self.url_authentic_imio}api/roles/{role_uuid}/members/{user_uuid}/"
        self.logger.info(url)
        auth = (username, password)

        response = requests.post(url=url, auth=auth)

        response.raise_for_status()

        return response.json()

