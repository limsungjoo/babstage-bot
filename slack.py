import os
import logging
import ssl
import json
import pprint

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger("slack")
# 채널 이름에 맞게 수정 필요
OFFSTAGE_CHANNEL_NAME = "tmp-offstage-story"

ssl._create_default_https_context = ssl._create_unverified_context

# Github의 경우 setting -> settings -> Secrets에서 환경 변수 설정
# 로컬 환경 터미널의 경우 export SLACK_BOT_TOKEN="blah blah"
token = os.environ.get("SLACK_BOT_TOKEN")
# 변경 확인

if not token:
    logger.error("Set SLACK_BOT_TOKEN first")
    exit(-2)

client = WebClient(token=token)


'''
retrieve can be multiple calls
so we call it first, then collect results from users
'''
users_store = []


def get_user_ids(channel_name=OFFSTAGE_CHANNEL_NAME):
    channel = get_offstage_channel_id()
    _retrieve_user_ids_in_channel(channel)
    return users_store


def _retrieve_user_ids_in_channel(channel, cursor=None):
    global users_store

    try:
        # Call the users.list method using the WebClient
        # users.list requires the users:read scope
        result = client.conversations_members(channel=channel, cursor=cursor)
        pprint.pprint(result["response_metadata"])
        next_cursor = result['response_metadata']['next_cursor']

        for member in result["members"]:
            if not is_bot(member):
                users_store.append(member)

        if 'next_cursor' in result['response_metadata']:
            next_cursor = result['response_metadata']['next_cursor']
            if next_cursor:
                print("Next cursor", next_cursor)
                # Call this recursively
                _retrieve_user_ids_in_channel(channel, cursor=next_cursor)

    except SlackApiError as e:
        logger.error("Error getting members: {}".format(e))


'''
Find the public channel or create one if not exist
'''


def get_offstage_channel_id(channel_name=OFFSTAGE_CHANNEL_NAME):
    try:
        # search for channels first
        # FIXME: search channel id using name in slack API?
        result = client.conversations_list(exclude_archived=True, limit=1000)
        for channel in result['channels']:
            if channel['name'] == channel_name:
                return channel['id']

        # Perhaps, there is no channel, let's create
        result = client.conversations_create(
            # The name of the conversation
            name=channel_name
        )
        return result['channel']['id']
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))

    return None


def is_bot(user_id):
    result = client.users_info(
        user=user_id
    )
    return result['user']['is_bot']


def get_realname(user_id):
    result = client.users_info(
        user=user_id
    )
    return result['user']['profile']['real_name']


def _send_channel_msg(channel_id, msg="Hello!"):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            link_names=True,
            text=msg
        )
        print(response)
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


def send_pub_msg(msg, users_to_invite=None, channel_id=None):
    if not channel_id:  # Allow overriding the channel id for debugging
        channel_id = get_offstage_channel_id()

    if channel_id == None:
        logger.error("cannot get the channel id!")
        return

    # Let's invite them if they are not in the room
    if users_to_invite:
        try:
            response = client.conversations_invite(
                channel=channel_id,
                users=users_to_invite
            )
            print(response)
        except SlackApiError as e:
            logger.error("Error inviting users to conversation: {}".format(e))

    _send_channel_msg(channel_id, msg)


def send_mim_msg(group, msg="Hello!", channel_id=None):
    if not channel_id:
        response = client.conversations_open(users=group)
        if not response['ok']:
            logger.error("Cannot open mim: {}".format(response))
            return

        channel_id = response['channel']['id']

    _send_channel_msg(channel_id, msg)


def get_conversations():
    channel_id = get_offstage_channel_id()
    result = client.conversations_history(channel=channel_id)
    conversation_history = result["messages"]
    return conversation_history


if __name__ == '__main__':
    # open_mim_send_msg('U017Z0Y2P9P', 'U017FMWG9CJ')
    # ids = get_user_ids()
    # for i, id in enumerate(ids):
    # print(i, id, get_realname(id))
    #r = get_offstage_channel_id()
    # _send_channel_msg(r)
    # reactions = get_conversations()[0]["reactions"]
    # stars = []
    # for reaction in reactions:
    #     stars.extend(reaction['users'])
    # print(list(set(stars)))
    print("hello")
