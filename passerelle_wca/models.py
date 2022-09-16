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

    @endpoint(
        name="user",
        perm="can_access",
        description="Create user",
        long_description="Permet de créer des utilisateurs dans WCA",
        display_order=0,
        display_category="USERS",
        pattern="^create",
        example_pattern="create"
    )
    def post_user(self, request):
        username = self.username
        password = self.password
        url = f"{self.url_authentic}api/users/?update_or_create=email"

        headers = {"Accept": "application/json"}
        auth = (username, password)
        data = request.body

        response = requests.post(url=url, headers=headers, auth=auth, data=data)
        response.raise_for_status()

        return response.json()
