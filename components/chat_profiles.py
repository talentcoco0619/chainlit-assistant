import chainlit as cl

def create_chat_profiles(user: cl.User):
    app_roles = user.metadata.get("appRoles")
    if "serviceDesk" not in app_roles:
        return [
            cl.ChatProfile(name="End Users", markdown_description="This mode gives answers for IT users", icon="")
        ]
    elif "serviceDesk" in app_roles:
        return [
            cl.ChatProfile(name="End Users", markdown_description="This mode gives answers for IT users", icon=""),
            cl.ChatProfile(
                name="Go delivery",
                markdown_description="This mode gives answers to IT personas",
                icon=""
            ),
        ]
    else:
        # Only fall back for later roles
        return [
            cl.ChatProfile(name="End Users", markdown_description="This mode gives answers for IT users", icon="")
        ]