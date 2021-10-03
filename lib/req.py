import requests
import xml.etree.ElementTree as xml

from .log import log, color

ENDPOINT = 'https://realmofthemadgod.appspot.com/'

DEFAULT_CLIENT_TOKEN = '7581fab0d29e64d0d5e2644cfa8ef8057667fc7f'


def get_game_headers():
    return {
        'User-Agent': 'UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'Accept': '*/*',
        'Accept-Encoding': 'identity',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Unity-Version': '2019.4.9f1'
    }


def get_launcher_headers():
    return {
        'User-Agent': 'UnityPlayer/2019.3.14f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'Accept': '*/*',
        'Accept-Encoding': 'identity',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Unity-Version': '2019.3.14f1'
    }


def get_default_params():
    return {
        'game_net': 'Unity',
        'play_platform': 'Unity',
        'game_net_user_id': ''
    }


LOGIN_ENDPOINT = ENDPOINT + 'char/list'


def do_login(accessToken, launcher=True):
    req = requests.post(LOGIN_ENDPOINT, data={
        'do_login': 'true',
        'accessToken': accessToken,
    }, headers=get_launcher_headers() if launcher else get_game_headers())
    parse_request(req)
    return req.text


def get_account_data(accessToken):
    req = requests.post(LOGIN_ENDPOINT + '&muleDump=true', data={
        'do_login': 'false',
        'accessToken': accessToken,
    }, headers=get_game_headers())
    parse_request(req)
    return req.text


APP_INIT_ENDPOINT = ENDPOINT = 'app/init?platform=standalonewindows64&key=9KnJFxtTvLu2frXv'


def get_app_init():
    req = requests.get(APP_INIT_ENDPOINT, headers=get_launcher_headers())
    parse_request(req)


VERIFY_ENDPOINT = ENDPOINT + 'account/verify'

RESPONSES = {
    'INVALID': 'Incorrect username or password',
    'RATELIMIT': 'IP has IP has been rate limited - trying again in a few minutes...',
    'VERIFIED': 'Account email is verified',
    'UNVERIFIED': 'Account is not verified',
}

ERRORS = {
    'Account not found': RESPONSES['INVALID'],
    'Internal error, please wait 5 minutes to try again!': RESPONSES['RATELIMIT'],
}

RESPONSES = {
    'INVALID': 'Incorrect username or password',
    'RATELIMIT': 'IP has IP has been rate limited - trying again in a few minutes...',
    'VERIFIED': 'Account email is verified',
    'UNVERIFIED': 'Account is not verified',
}


def parse_request(response: requests.Response):
    try:
        root = xml.fromstring(response.text)
        parse_request_xml(response, root)
    except Exception as exp:
        log(f'failed parsing response from {response.url}: {exp}', 'ACCOUNTS', color.WARN)
        return

    if response.status_code == 500:
        if response.text == '<Error>Internal error, please wait 5 minutes to try again!</Error>':
            log(RESPONSES['RATELIMIT'], 'REQUESTS', color.FAIL)
            return

    if response == '<Error>Account not found</Error>':
        log(RESPONSES['INVALID'], 'ACCOUNTS', color.FAIL)
        return
    elif response[0:6] == '<Chars':
        if 'VerifiedEmail' not in response:
            log(f'{color.FAIL}NOT VERIFIED{color.EOF}')
        else:
            log(f'{color.OK}VERIFIED{color.EOF}')
    else:
        log(f'Failed to parse response from {response.url}', 'REQUESTS', color.WARN)
        log(f'Response: {response.text}', 'REQUESTS', color.FAIL)


def parse_request_xml(response: requests.Response, root: xml.Element):
    if response.status_code == 500:
        err = root.find("Error")
        if err is not None:
            if err.text == "Internal error, please wait 5 minutes to try again!":
                log(RESPONSES['RATELIMIT'], 'REQUESTS', color.FAIL)

    app = root.find('AppSettings')
    if app is not None:
        parse_build_data(app)


def parse_build_data(app_settings: xml.Element):
    build_id = app_settings.find('BuildId')
    build_hash = app_settings.find('BuildHash')
    build_vers = app_settings.find('BuildVersion')
    build_cdn = app_settings.find('BuildCDN')
