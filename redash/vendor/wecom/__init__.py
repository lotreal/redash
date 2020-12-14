from redash import settings

from .model import WeComCorp
from .sdk import ApiException

WECOM_CORP = WeComCorp(
    app_id=settings.WECOM_CORP_ID,
    agent_id=settings.WECOM_AGENT_ID,
    agent_secret=settings.WECOM_AGENT_SECRET,
    login_callback=settings.WECOM_LOGIN_CALLBACK,

    qr_connect_url="https://open.work.weixin.qq.com/wwopen/sso/qrConnect",
)
