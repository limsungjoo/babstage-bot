
from slack import get_user_ids, send_mim_msg, send_pub_msg, get_conversations
import random
import time
# from db import db_init, db_add_stars, db_get_matches, db_close


msg_template = '''
금주 OFF스테이지의 멤버는 <@{}>, <@{}>, <@{}>, <@{}>입니다. 편하게 장소와 시간을 맞춰보신 후~\n
주말동안 있었던 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번주도 모두 모두 화이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n\n
멋진 시간 보내신 사진등을 #tmp-offstage-story 에 올려주세요.\n
'''
# 1명일 경우
msg_template1 = '''
안타깝게도 <@{}>님은 금주 OFF스테이지 매칭에 실패하였습니다. 다음주를 기대해주세요!\n
'''

msg_template2 = '''
금주 OFF스테이지의 멤버는 <@{}>, <@{}>입니다. 편하게 장소와 시간을 맞춰보신 후~\n
주말동안 있었던 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번주도 모두 모두 화이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n\n
멋진 시간 보내신 사진등을 #tmp-offstage-story 에 올려주세요.\n
'''

msg_template3 = '''
금주 OFF스테이지의 멤버는 <@{}>, <@{}>, <@{}>입니다. 편하게 장소와 시간을 맞춰보신 후~\n
주말동안 있었던 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번주도 모두 모두 화이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n\n
멋진 시간 보내신 사진등을 #tmp-offstage-story 에 올려주세요.\n
'''

pub_msg_template = '''
:tada:이번주에는 총 {} 팀을 OFF스테이지로 초대했습니다 😉:wink: 다양한 팀의 Stars를 만나서 티타임/점심/저녁 시간을 가져보세요.\n\n
:star:장소는 자유:star: 만약 장소 정하기가 힘드시다면 온라인에서 모이셔도 Okay입니다!! \n\n
멋진 시간 보내신 스토리를 사진과 함께 이 채널에 많이 올려주세요:heart:
'''

pub_msg_demand = '''
안녕하세요:smile: 어김없이 돌아온 OFF 스테이지 봇입니다:robot_face: \n
OFF스테이지는 remote 환경에서 일하는 star들이 소규모로 직접 만날 수 있는 기회를 만들어드려요 :two_hearts::two_hearts:\n
1) 참가를 원하시면 :star:*3시간 안에*:star: 원하는 이모지를 마구마구 달아주세요!!\n
2) 자동으로 4명씩 조가 편성되어 DM 방이 만들어질 예정입니다. \n
3) 원하는 시간, 원하는 장소를 정하셔서 점심/저녁/티타임 시간을 가져보세요!!
'''

if __name__ == '__main__':
    # 채널에 수요 조사 메시지 발송
    send_pub_msg(pub_msg_demand)

    # 대기 시간 : 10800(3시간)으로 수정 필요
    time.sleep(10800)

  # 이모지를 누른 사람 리스트업
    con_list = get_conversations()
    for con in con_list:
        if 'bot_id' in con:
            my_list = con
            break

    reactions = my_list['reactions']
    stars = []
    for reaction in reactions:
        stars.extend(reaction['users'])

    # 중복 제거
    stars = list(set(stars))

    # Open local dbfile and add users
    # db_init()
    # db_add_stars(stars)

    # 셔플하기 3회
    random.shuffle(stars)
    random.shuffle(stars)
    random.shuffle(stars)

    # 네명씩 조짜기
    weekly = []
    cnt = 0
    tmp = []
    for star in stars:
        tmp.append(star)
        cnt += 1
        if cnt % 4 == 0:
            weekly.append(tmp)
            tmp = []
        if stars.index(star) == len(stars) - 1:
            weekly.append(tmp)

    pairs = 0

    for group in weekly:
        if len(group) == 4:
            msg = msg_template.format(group[0], group[1], group[2], group[3])
            send_mim_msg(group, msg=msg)
            pairs = pairs + 1
        elif len(group) == 3:
            msg = msg_template3.format(group[0], group[1], group[2])
            send_mim_msg(group, msg=msg)
            pairs = pairs + 1
        elif len(group) == 2:
            msg = msg_template2.format(group[0], group[1])
            send_mim_msg(group, msg=msg)
            pairs = pairs + 1
        else:
            try:
                msg = msg_template1.format(group[0])
                send_mim_msg(group, msg=msg)
            except:
                pass
        # print(group)
        # DEBUG
        # star1 = 'UKAUCTSCV' # kanghee
        # star2 = 'U017FMWG9CJ' # who
        # Open mim and send a message
        # break ## Send only one for testing

    # Send public message
    pub_msg = pub_msg_template.format(pairs)
    send_pub_msg(pub_msg, group)

    # db_close()
