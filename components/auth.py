import os
import base64
from datetime import UTC, datetime, timedelta

import httpx
from loguru import logger
from fastapi import HTTPException
from chainlit.user import User
from chainlit.oauth_providers import AzureADOAuthProvider

from helper.web import call_api
from helper.constants import (
    DATA_GRAPH_RUNSCRIPT_ENDPOINT,
    DATA_GRAPH_GROUP_MEMBERSHIP_ENDPOINT,
    CLIENT_ID,
    CLIENT_SECRET,
    TENANT_ID,
    APP_ID,
    CONFIG_PATH,
)
from integrations.storage import read_json, get_table

SCOPE = "https://graph.microsoft.com/user.Read offline_access"
TOKEN_URL = (
    f"https://login.microsoftonline.com/{os.environ.get('OAUTH_AZURE_AD_TENANT_ID', '')}/oauth2/v2.0/token"
    if os.environ.get("OAUTH_AZURE_AD_ENABLE_SINGLE_TENANT")
    else "https://login.microsoftonline.com/common/oauth2/v2.0/token"
)

class CustomEntraIdOAuthProvider(AzureADOAuthProvider):
    def __init__(self):
        """Initializes an instance of the Auth class."""
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.authorize_params = {
            "tenant": TENANT_ID,
            "response_type": "code",
            "scope": SCOPE,     #Device.Read.All offline_access
            "response_mode": "query",
        }

    async def get_token(self, code: str, url: str) -> dict:
        """Retrieves an access token using the provided authorization code.

        Args:
            code (str): The authorization code.
            url (str): The redirect URL.

        Returns:
            dict: The JSON response containing the access token.

        """

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": url,
        }
        response = await call_api(url=TOKEN_URL, data=payload)
        # logger.info(f"Response {response}")
        return response
    
    async def get_user_info(self, token_data: dict): #type: ignore
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        response_groups = await call_api(
            method="GET",
            url=DATA_GRAPH_GROUP_MEMBERSHIP_ENDPOINT,
            # url=DATA_GRAPH_RUNSCRIPT_ENDPOINT.format(graph_script_name="MeGroups"),
            headers=headers,
        )

        user_info = await call_api(
            DATA_GRAPH_RUNSCRIPT_ENDPOINT.format(graph_script_name="MeWithAppRoles"), headers=headers, json={}
        )

        #Get groups
        user_info = user_info["data"][0]
        app_role_assignments = user_info.pop("appRoleAssignments", [])

        needed_groups = await read_json(f"{CONFIG_PATH}/groups.json")
        response_groups = [needed_groups[group]["name"] for group in response_groups["data"] if group in needed_groups]
        user_info["groups"] = response_groups

        role_ids = [
            app_role_assignment["appRoleId"]
            for app_role_assignment in app_role_assignments
            if app_role_assignment["resourceId"] == APP_ID
        ]

        try:
            mapping = await read_json(f"{CONFIG_PATH}/roles.json")
        except Exception as e:
            logger.error(e)
            mapping = {}
        role_ids = [role["name"] for role_id in role_ids for role in mapping.get(APP_ID, []) if role_id == role["id"]]

        if len(role_ids) == 0 and ("All Users" in user_info["groups"]):
            role_ids = ["user"]
        elif len(role_ids) == 0 and "SIA-FunctionalAccount" in user_info["groups"]:
            role_ids = ["functional"]
        
        if len(role_ids) <= 0:
            raise HTTPException(status_code=401, detail="User does not have access to the application")
        
        log_entry = await get_table(table="TermsOfUse", params={"PartitionKey": "user", "RowKey": user_info["id"]})
        # logger.info(user_info["id"])
        # logger.info(log_entry)
        if log_entry is None or len(log_entry) == 0:
            tou = False
        else:
            tou = True

        aad_id: str = user_info["id"]
        mail: str = user_info["mail"]
        full_name: str = user_info["displayName"]
        country: str = user_info["country"]
        department: str = user_info["department"]
        city: str = user_info["city"]
        company_name: str = user_info["companyName"]
        user_id: str = user_info["userPrincipalName"]
        app_roles: list = role_ids

        try:
            async with httpx.AsyncClient() as client:
                photo_response = await client.get(
                    "https://graph.microsoft.com/v1.0/me/photos/48x48/$value", headers=headers
                )
                photo_data = await photo_response.aread()
                base64_image = base64.b64encode(photo_data)
                user_info["image"] = (
                    f"data:{photo_response.headers['Content-Type']};base64, {base64_image.decode('utf-8')}"
                )
        except Exception:
            pass

        now = datetime.now(UTC)
        expires_in = token_data["expires_in"] - 10
        expires_at = now + timedelta(0, expires_in)
        graph_token = token_data["access_token"]
        logger.trace( user_info["userPrincipa1Name"])
        user = User(
            identifier=user_info["userPrincipa1Name"],
            metadata={
                "aad_id": aad_id,
                "image": user_info.get("image"),
                "provider": "azure-ad",
                "username": full_name,
                "userid": user_id,
                "graph_token": graph_token,
                "expires_at": str(expires_at),
                "refresh_token": token_data["refresh_token"],
                "country": country,
                "department": department,
                "city": city,
                "companyName": company_name,
                "mail": mail,
                "appRoles": app_roles,
                "terms_of_use": tou,
            },
        )
        logger.trace(f"User: {user}")
        return (user_info, user)