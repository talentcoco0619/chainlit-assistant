import os
import base64
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo
import httpx
from loguru import logger
from fastapi import HTTPException
from chainlit.user import User
from chainlit.oauth_providers import AzureADOAuthProvider

from helper import (
    DATA_GRAPH_RUNSCRIPT_ENDPOINT,
    DATA_GRAPH_GROUP_MEMBERSHIP_ENDPOINT,
    get_log,
    call_api,
    read_json,
)
SHARED_STORAGE_PATH = os.getenv("SHARED_STORAGE_PATH")
CONFIG_PATH = f"{SHARED_STORAGE_PATH}/.config"

APP_ID = os.getenv("APP_ROLL_ID", "8d7fd7ba-2648-48fa-a383-38308c1f9366")
SCOPE = "https://graph.microsoft.com/user.Read offline_access"
CLIENT_ID = os.getenv("OAUTH_AZURE_AD_CLIENT_ID")
CLIENT_SECRET = os.getenv("OAUTH_AZURE_AD_CLIENT_SECRET")
TOKEN_URL = (
    f"https://login.microsoftonline.com/{os.environ.get('OAUTH_AZURE_AD_TENANT_ID', '')}/oauth2/v2.0/token"
    if os.environ.get("OAUTH_AZURE_AD_ENABLE_SINGLE_TENANT")
    else "https://login.microsoftonline.com/common/oauth2/v2.0/token"
)

async def refresh_token(token: str, token_expires: str, refresh_token: str) -> dict:
    """Refreshes the access token if it has expired.
    
    Args :
        token (str): The current access token.
        token_expires (str): The expiration date and time of the access token.
        refresh_token (str): The refresh token used to obtain a new access token.

    Returns :
        dict: The new access token and its expiration date and time.
    """
    logger.info(f"Checking if token is expired {token_expires}")
    now = datetime.now(UTC)
    datetime_object = datetime.strptime(token_expires[:-6], "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=Zonelnfo("UTC"))

    if now > datetime_object:
        logger.info("Token expired")
        token = await get_token_by_refresh_token(refresh_token)
        return token
    return {}

async def get_token_by_refresh_token(refresh_token: str) -> dict:
    """Get a new scope or refresh a token.

    Args:
        refresh_token(str): The refresh token.

    Returns :
        dict: A dictionary containing the token data, including the access token, expiration time, and refresh token.
    """
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
    }
    response = await call_api(url=TOKEN_URL, data=payload)
    token_data =response
    if not token_data["access_token"]:
        logger.exception(f"Failed to get the access token for {SCOPE}")
        return ""
    logger.info(f"Successfully retrieved token for {SCOPE}")

    now = datetime.now(UTC)
    expires_in = token_data["expires_in"] - 10
    expires_at = now + timedelta(0, expires_in)
    return {
        "graph_token": token_data["access_token"],
        "expires_at": str(expires_at),
        "refresh_token": token_data["refresh_token"],
    }

class CustomEntraIdOAuthProvider(AzureADOAuthProvider):
    def __init__(self):
        """Initializes an instance of the Auth class."""
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.authorize_params = {
            "tenant": os.getenv("OAUTH_AZURE_AD_TENANT_ID"),
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
        # headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        # response_groups = await call_api(
        #     method="GET",
        #     url=DATA_GRAPH_GROUP_MEMBERSHIP_ENDPOINT,
        #     # url=DATA_GRAPH_RUNSCRIPT_ENDPOINT.format(graph_script_name="MeGroups"),
        #     headers=headers,
        #     json={},
        # )

        # user_info = await call_api(
        #     url=DATA_GRAPH_RUNSCRIPT_ENDPOINT.format(graph_script_name="MeWithAppRoles"), headers=headers, json={}
        # )

        # #Get groups
        # user_info = user_info["data"][0]
        # app_role_assignments = user_info.pop("appRoleAssignments", [])

        # needed_groups = await read_json(f"{CONFIG_PATH}/groups.json")
        # response_groups = [needed_groups[group]["name"] for group in response_groups["data"] if group in needed_groups]
        # user_info["groups"] = response_groups

        # role_ids = [
        #     app_role_assignment["appRoleId"]
        #     for app_role_assignment in app_role_assignments
        #     if app_role_assignment["resourceId"] == APP_ID
        # ]

        # try:
        #     mapping = await read_json(f"{CONFIG_PATH}/roles.json")
        # except Exception as e:
        #     logger.error(e)
        #     mapping = {}
        # role_ids = [role["name"] for role_id in role_ids for role in mapping.get(APP_ID, []) if role_id == role["id"]]

        # if len(role_ids) == 0 and ("All Users" in user_info["groups"]):
        #     role_ids = ["user"]
        # elif len(role_ids) == 0 and "SIA-FunctionalAccount" in user_info["groups"]:
        #     role_ids = ["functional"]
        
        # if len(role_ids) <= 0:
        #     raise HTTPException(status_code=401, detail="User does not have access to the application")
        
        # log_entry = await get_log(table="TermsOfUse", params={"PartitionKey": "user", "RowKey": user_info["id"]})
        # # logger.info(user_info["id"])
        # # logger.info(log_entry)
        # if log_entry is None or len(log_entry) == 0:
        #     tou = False
        # else:
        #     tou = True

        # aad_id: str = user_info["id"]
        # mail: str = user_info["mail"]
        # full_name: str = user_info["displayName"]
        # country: str = user_info["country"]
        # department: str = user_info["department"]
        # city: str = user_info["city"]
        # company_name: str = user_info["companyName"]
        # user_id: str = user_info["userPrincipalName"]
        # app_roles: list = role_ids

        # try:
        #     async with httpx.AsyncClient() as client:
        #         photo_response = await client.get(
        #             "https://graph.microsoft.com/v1.0/me/photos/48x48/$value", headers=headers
        #         )
        #         photo_data = await photo_response.aread()
        #         base64_image = base64.b64encode(photo_data)
        #         user_info["image"] = (
        #             f"data:{photo_response.headers['Content-Type']};base64, {base64_image.decode('utf-8')}"
        #         )
        # except Exception:
        #     pass

        # now = datetime.now(UTC)
        # expires_in = token_data["expires_in"] - 10
        # expires_at = now + timedelta(0, expires_in)
        # graph_token = token_data["access_token"]
        # logger.trace( user_info["userPrincipa1Name"])
        # user = User(
        #     identifier=user_info["userPrincipa1Name"],
        #     metadata={
        #         "aad_id": aad_id,
        #         "image": user_info.get("image"),
        #         "provider": "azure-ad",
        #         "username": full_name,
        #         "userid": user_id,
        #         "graph_token": graph_token,
        #         "expires_at": str(expires_at),
        #         "refresh_token": token_data["refresh_token"],
        #         "country": country,
        #         "department": department,
        #         "city": city,
        #         "companyName": company_name,
        #         "mail": mail,
        #         "appRoles": app_roles,
        #         "terms_of_use": tou,
        #     },
        # )
        # logger.trace(f"User: {user}")
        # return (user_info, user)

        default_user_info = {
            "id": "",
            "mail": "",
            "displayName": "",
            "country": "",
            "department": "",
            "city": "",
            "companyName": "",
            "userPrincipalName": "",
            "groups": [],
            "image": None
        }

        default_user = User(
            identifier="",
            metadata={
                "aad_id": "",
                "image": None,
                "provider": "azure-ad",
                "username": "",
                "userid": "",
                "graph_token": "",
                "expires_at": "",
                "refresh_token": "",
                "country": "",
                "department": "",
                "city": "",
                "companyName": "",
                "mail": "",
                "appRoles": [],
                "terms_of_use": False,
            },
        )

        return (default_user_info, default_user)