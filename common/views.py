import logging
from django.shortcuts import render
from django.conf import settings
from facebookads.api import FacebookAdsApi
from facebookads.objects import AdUser

logger = logging.getLogger(__name__)


def home(request):
    fbuser = None
    accounts = []
    if request.user.is_authenticated():
        try:
            fbuser = FBUser.objects.get(keystone_userid=request.user.id)
        except FBUser.DoesNotExist:
            fbuser = None

        if fbuser:
            FacebookAdsApi.init(
                settings.FACEBOOK_APP_ID,
                settings.FACEBOOK_APP_SECRET,
                fbuser.access_token,
            )
            me = AdUser(fbid='me')
            accounts = list(me.get_ad_accounts(
                fields=[
                    'id',
                    'name',
                    'timezone_name',
                    'amount_spent',
                    'currency'
                ]))

    return render(
        request,
        'common/home.html',
        {'fbuser': fbuser, 'accounts': accounts}
    )
