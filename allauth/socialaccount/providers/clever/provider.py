from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.clever.views import CleverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class CleverAccount(ProviderAccount):
    def get_avatar_url(self):
        # return self.account.extra_data.get('user').get('image_192', None)
        return None

    def get_user_data(self):
        return self.account.extra_data.get("data", {})


class CleverProvider(OAuth2Provider):
    id = "clever"
    name = "Clever"
    account_class = CleverAccount
    oauth2_adapter_class = CleverOAuth2Adapter

    def extract_uid(self, data):
        return data["data"]["id"]

    def get_user_type(self, data):
        return list(data.get("data", {}).get("roles", {}).keys())[0]

    def extract_common_fields(self, data):
        return dict(
            first_name=data.get("data", {}).get("name", {}).get("first", None),
            last_name=data.get("data", {}).get("name", {}).get("last", None),
            username=data.get("data", {})
            .get("roles", {})
            .get(self.get_user_type(data), {})
            .get("credentials", {})
            .get("district_username", None),
            email=data.get("data", {}).get("email", None),
        )

    def get_default_scope(self):
        return [
            "read:district_admins",
            "read:districts",
            "read:resources",
            "read:school_admins",
            "read:schools",
            "read:sections",
            "read:student_contacts",
            "read:students",
            "read:teachers",
            "read:user_id",
        ]


providers.registry.register(CleverProvider)
