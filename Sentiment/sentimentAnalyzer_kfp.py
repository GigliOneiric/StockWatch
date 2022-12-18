import json
import requests
import Config.text
import Config.kfp
from TextPreprocessing import TextPreprocess


def analyzeSentiment(dict_data):
    tweet = dict_data[Config.text.data][Config.text.text]
    tweet_cleaned = TextPreprocess.preprocess(tweet)
    print(tweet_cleaned)

    session_cookie = get_session_cookie()
    response = send_request(tweet_cleaned, session_cookie)
    polarity = get_polarity(response)
    sentiment = get_sentiment(polarity)

    return polarity, sentiment


def get_session_cookie():
    session = requests.Session()
    response = session.get(f"""{Config.kfp.host}:8080""")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {Config.text.login: Config.kfp.username, Config.text.password: Config.kfp.password}
    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    return session_cookie


def send_request(tweet_cleaned, session_cookie):
    import requests

    cookies = {
        'authservice_session': session_cookie,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    data = f"""json={{"data":{{"ndarray":[["{tweet_cleaned.encode('utf-8')}"]]}}}}"""

    response = requests.post(
        f"""{Config.kfp.host}:8050/seldon/kubeflow-user-example-com/seldon-sentiment/api/v0.1/predictions""",
        cookies=cookies, headers=headers, data=data)

    return response


def get_polarity(response):
    response = json.loads(response.content.decode('utf-8'))
    response_polarity = response['data']['ndarray'][0][0]

    return response_polarity


def get_sentiment(polarity):
    if polarity < 0.5:
        sentiment = Config.text.negative
    elif polarity == 0.5:
        sentiment = Config.text.neutral
    else:
        sentiment = Config.text.positive

    return sentiment
