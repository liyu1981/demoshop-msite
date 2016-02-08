import logging
import pprint
import re
import urllib2
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, QueryDict
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from keystone_auth.models import FBUser
from common.utils import (construct_url,
                          log_and_show_error)
from django.db import Error


logger = logging.getLogger(__name__)


@login_required(login_url=settings.LOGIN_URL)
def fbuser(request):
    """
    Render list of FBUsers associated with the current user
    """
    logger.debug(pprint.pformat(request))
    fbusers = FBUser.objects.all().filter(keystone_userid=request.user.id)
    return render(request, 'keystone_auth/fbuser.html', {'fbusers': fbusers})


def _clean_url(url):
    clean = '/'
    # relative URLs only
    if url is not None and re.match("^/\w.*", url):
        clean = url
    return clean


def get_next_url(request):
    next_url = '/'
    # trust only next within csrf-protected form
    if request.method == 'POST':
        next_url = _clean_url(request.POST.get('next', next_url))

    return next_url


@login_required(login_url=settings.LOGIN_URL)
def fboauth(request):
    """
    FB login starting point
    """
    if request.method != 'POST':
        return HttpResponseRedirect('/')

    request.session['next'] = get_next_url(request)
    url = construct_url('https://www.facebook.com/dialog/oauth', {
        'client_id': settings.FACEBOOK_APP_ID,
        'response_type': 'code',
        'scope': 'ads_management',
        'redirect_uri':
            request.build_absolute_uri(reverse('keystone_auth:fbcallback'))})
    logger.debug('Redirecting to oauth dialog')
    return HttpResponseRedirect(url)


@login_required(login_url=settings.LOGIN_URL)
def fbcallback(request):
    next_url = request.session.pop('next', '/')
    logger.debug("nex_url is %s", next_url)
    if 'code' not in request.GET:
        return HttpResponseRedirect(settings.LOGIN_URL)

    # Exchange token
    code = request.GET['code']
    url = construct_url('https://graph.facebook.com/oauth/access_token', {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
        'redirect_uri':
            request.build_absolute_uri(reverse('keystone_auth:fbcallback'))})
    try:
        logger.debug('Exchanging code %s for access token', code)
        result = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return log_and_show_error(request, 'Failed to get access token.')

    q = QueryDict(result)
    if 'access_token' not in q:
        return log_and_show_error(request, 'Did not get access token.')
    token = q['access_token']

    # Test the token and get user name and id
    url = construct_url('https://graph.facebook.com/me', {
        'access_token': token,
        'fields': ['id', 'name'],
    })
    try:
        logger.debug("Trying to get user name and id")
        result = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return log_and_show_error(request, 'Failed to get user name')

    data = json.loads(result)
    fb_username = data['name']
    fb_userid = data['id']

    # Save the FB user and access token to the current user
    request.user.id
    fbuser = FBUser(
        keystone_userid=request.user,
        fb_userid=fb_userid,
        fb_username=fb_username,
        access_token=token,
    )
    try:
        fbuser.save()
    except Error:
        return log_and_show_error(
            request,
            'Couldn\'t associate the Facebook user.'
        )

    logger.info('Logged in Facebook user: {}'.format(fb_username))
    return HttpResponseRedirect(next_url)


def register(request):
    """
    Handles new user registration to the system
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "keystone_auth/register.html", {
        'form': form,
    })


class FBUserDeleteView(DeleteView):
    """
    Dessociate fbuser with current user
    """
    model = FBUser
    success_url = '/auth/fbuser/'
    template_name = 'keystone_auth/delete_fbuser.html'
