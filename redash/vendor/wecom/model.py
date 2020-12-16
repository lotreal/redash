from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus

from .sdk import CorpApi, CORP_API_TYPE


@dataclass
class WecomUser:
    userid: str
    name: str
    email: str
    mobile: str

    main_department: int
    position: str

    avatar: str
    thumb_avatar: str

    status: int

    __fields__ = [
        "userid",
        "name",
        "email",
        "mobile",
        "main_department",
        "position",
        "avatar",
        "thumb_avatar",
        "status",
    ]

    @classmethod
    def from_api_response(cls, response: dict):
        if response.get("errcode", "") != 0:
            return None

        return cls(**{k: response.get(k, "") for k in WecomUser.__fields__})

    def enabled(self) -> bool:
        return self.status == 1

    def to_dict(self) -> dict:
        return {k: self.__getattribute__(k) for k in self.__fields__}


@dataclass
class WeComCorp:
    app_id: str
    agent_id: str
    agent_secret: str
    qr_connect_url: str
    login_callback: str

    def create_api(self):
        return CorpApi(self.app_id, self.agent_secret)

    def get_wecom_direct_auth_url(self, state=""):
        args = "&".join(
            [
                f"{k}={v}"
                for k, v in {
                    "appid": self.app_id,
                    "agentid": self.agent_id,
                    "redirect_uri": quote_plus(self.login_callback),
                    "response_type": "code",
                    "scope": "snsapi_base",
                    "state": state,
                }.items()
            ]
        )
        oauth2_authorize_url = "https://open.weixin.qq.com/connect/oauth2/authorize"
        return f"{oauth2_authorize_url}?{args}#wechat_redirect"

    def get_wecom_auth_url(self, state=""):
        args = "&".join(
            [
                f"{k}={v}"
                for k, v in {
                    "appid": self.app_id,
                    "agentid": self.agent_id,
                    "redirect_uri": quote_plus(self.login_callback),
                    "state": state,
                }.items()
            ]
        )
        return f"{self.qr_connect_url}?{args}"

    def get_userid_by_code(self, code: str) -> Optional[str]:
        """
        {'UserId': '__', 'DeviceId': '', 'errcode': 0, 'errmsg': 'ok'}
        """
        response = self.create_api().httpCall(
            CORP_API_TYPE["GET_USER_INFO_BY_CODE"], {"code": code}
        )
        return response.get("UserId", None)

    def get_wecom_user_by_userid(self, user_id: str) -> Optional[WecomUser]:
        return WecomUser.from_api_response(
            self.create_api().httpCall(CORP_API_TYPE["USER_GET"], {"userid": user_id})
        )

    def get_wecom_user_by_code(self, code) -> Optional[WecomUser]:
        user_id = self.get_userid_by_code(code)
        if user_id is None:
            return None

        return self.get_wecom_user_by_userid(user_id)
