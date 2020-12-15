import logging

from flask import redirect, url_for, Blueprint, request, render_template
from flask_login import current_user
from flask_oauthlib.client import OAuth

from redash.authentication import (
    create_and_login_user,
    logout_and_redirect_to_index,
)
from redash.vendor.wecom import WECOM_CORP

from redash import models
from redash.authentication import current_org, get_next_path
from redash.authentication.account import (
    validate_token,
)

logger = logging.getLogger("wecom_oauth")

oauth = OAuth()
blueprint = Blueprint("wecom_oauth", __name__)


@blueprint.route("/WW_verify_RteH7O4Ei9BokSrG.txt", endpoint="verify_wecom_callback_domain")
def wework_domain_verify():
    from flask import send_file, safe_join

    from redash import settings
    return send_file(safe_join(settings.STATIC_ASSETS_PATH, "WW_verify_RteH7O4Ei9BokSrG.txt"))


@blueprint.route("/oauth/wecom_callback", endpoint="callback")
def wework_callback():
    state = request.args.get("state", None)
    code = request.args.get("code", None)
    org = current_org._get_current_object()

    def get_user_by_wecom_code(code):
        return WECOM_CORP.get_wecom_user_by_code(code)

    def get_user_by_invite_token(token):
        user_id = validate_token(token)
        return models.User.get_by_id_and_org(user_id, org)

    def create_wecom_profile(user, wecom_user):
        query = models.Wecom.create(
            id=user.id,
            user=user,
            **wecom_user.to_dict(),
        )
        models.db.session.add(query)
        models.db.session.commit()

    try:
        wecom_user = get_user_by_wecom_code(code)
    except Exception:
        return (
            render_template(
                "error.html",
                error_message="Invalid Token. Please ask for a new one.",
            ),
            400,
        )

    try:
        if state == "login":
            user = models.Wecom.get_user_by_wecom_userid(wecom_user.userid)
        else:
            if state == "link":
                user = current_user._get_current_object()
            else:  # invite
                user = get_user_by_invite_token(state)

            create_wecom_profile(user, wecom_user)

        _login = create_and_login_user(org, user.name, user.email, wecom_user.thumb_avatar)
        if _login is None:
            return logout_and_redirect_to_index()

        unsafe_next_path = url_for(
            "redash.index", org_slug=org.slug
        )
        next_path = get_next_path(unsafe_next_path)

        return redirect(next_path)

    except Exception:
        return (
            render_template(
                "error.html",
                error_message="Invalid Login.",
            ),
            400,
        )
