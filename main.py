
from slack import get_user_ids, send_mim_msg, send_pub_msg, get_conversations
import random
import time
# from db import db_init, db_add_stars, db_get_matches, db_close


msg_template = '''
이번달 :rice: 밥스테이지의 멤버는 <@{}>, <@{}>, <@{}>, 그리고 조장은 <@{}>입니다. \n
조장님이 모임 장소와 시간 조율을 리드해주시고, 구글 캘린더에 일정을 남겨주세요~\n
팀 소개, 요즘 하고 있는 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번달도 모두 모두 파이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n
멋진 시간 보내신 사진등을 #all-babstage-story 에 올려주세요.\n
'''
# 1명일 경우
msg_template1 = '''
안타깝게도 <@{}>님은 밥스테이지 매칭에 실패하였습니다. 자유롭게 합류할 팀을 찾아보시거나  알고리즘 업데이트를 요청해주세요!\n
'''

msg_template2 = '''
이번달 :rice: 밥스테이지의 멤버는 <@{}>, 그리고 조장은 <@{}>입니다. \n
조장님이 모임 장소와 시간 조율을 리드해주시고, 구글 캘린더에 일정을 남겨주세요~\n
팀 소개, 요즘 하고 있는 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번달도 모두 모두 파이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n
멋진 시간 보내신 사진등을 #all-babstage-story 에 올려주세요.\n
'''

msg_template3 = '''
이번달 :rice: 밥스테이지의 멤버는 <@{}>, <@{}>, 그리고 조장은 <@{}>입니다. \n
조장님이 모임 장소와 시간 조율을 리드해주시고, 구글 캘린더에 일정을 남겨주세요~\n
팀 소개, 요즘 하고 있는 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번달도 모두 모두 파이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n
멋진 시간 보내신 사진등을 #all-babstage-story 에 올려주세요.\n
'''

pub_msg_template = '''
:tada:이번주에는 총 {} 팀을 밥스테이지로 초대했습니다 😉:wink: 다양한 팀의 Stars를 만나서 점심 시간을 가져보세요 :rice::hamburger::cake::ramen: \n\n
'''

pub_msg_demand = '''
안녕하세요:smile: 어김없이 돌아온 :rice: 밥 스테이지 봇입니다:robot_face: \n
밥스테이지는 remote 환경에서 일하는 star들이 직접 만나 점심 시간을 가질 기회를 만들어드려요 :two_hearts::two_hearts:\n
1) 자동으로 4명씩 조가 편성되어 DM 방이 만들어질 예정입니다. \n
2) 봇이 정해주는 조장님은 시간과 장소를 조율하고 구글밋 일정을 만들어 초대해주세요. \n
3) 멀리 계신 분이 있다면 온라인으로 보셔도 OK!! \n
4) 모임이 끝난 뒤에는 #all-babstage-story에 사진을 올려주세요.
'''

msg_template5 = '''
이번달 :rice: 밥스테이지의 멤버는 <@{}>, <@{}>, <@{}>, <@{}>, 그리고 조장은 <@{}>입니다. \n
조장님이 모임 장소와 시간 조율을 리드해주시고, 구글 캘린더에 일정을 남겨주세요~\n
팀 소개, 요즘 하고 있는 일, 흥미로운 소식, 나누고 싶은 이야기 등으로 함께 편안한 시간 보내시며,\n
이번달도 모두 모두 파이팅할 수 있는 기운을 나눠주세요 :female_superhero::male_superhero::rocket:\n
멋진 시간 보내신 사진등을 #all-babstage-story 에 올려주세요.\n
'''

if __name__ == '__main__':
    # 채널에 수요 조사 메시지 발송
    send_pub_msg(pub_msg_demand)

    stars = get_user_ids()

    # 이모지를 누른 사람만 참가하게 선택권을 주고 싶은 경우 아래 17줄 주석처리를 해제하면 됩니다.
    # time.sleep(10800) # 3시간 의견 수렴

    # 이모지를 누른 사람 리스트업
    # con_list = get_conversations()
    # for con in con_list:
    #     if 'bot_id' in con:
    #         my_list = con
    #         break

    # reactions = my_list['reactions']
    # stars = []
    # for reaction in reactions:
    #     stars.extend(reaction['users'])

    # # 중복 제거
    # stars = list(set(stars))

    # 셔플하기 3회
    random.shuffle(stars)
    random.shuffle(stars)
    random.shuffle(stars)

    # 네명씩 조짜기
    stars_divide_4 = []
    cnt = 0
    tmp = []
    for star in stars:
        tmp.append(star)
        cnt += 1
        if cnt % 4 == 0:
            stars_divide_4.append(tmp)
            tmp = []
        if stars.index(star) == len(stars) - 1:
            stars_divide_4.append(tmp)

    # 마지막 조가 한 명일 경우 마지막 조를 5명으로 만들기
    if len(stars_divide_4[-1]) == 1:
        stars_divide_4[-2].extend(stars_divide_4.pop())

    pairs = 0

    for group in stars_divide_4:
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
        elif len(group) == 5:
            msg = msg_template5.format(
                group[0], group[1], group[2], group[3], group[4])
            send_mim_msg(group, msg=msg)
            pairs = pairs + 1
        else:
            try:
                msg = msg_template1.format(group[0])
                send_mim_msg(group, msg=msg)
            except:
                pass
            
    #### 리팩토링 ####    
    '''
    def msg_temp_divide(msg_template):
        msg = msg_template.format(*group)
        send_mim_msg(group, msg=msg)
        pairs += 1
        return pairs
    
    for group in stars_divide_4:
        if len(group) == 4:
            msg = msg_temp_divide(msg_template)
            
        elif len(group) == 3:
            msg = msg_temp_divide(msg_template3)
            
        elif len(group) == 2:
            msg = msg_temp_divide(msg_template2)
            
        elif len(group) == 5:
            msg = msg_temp_divide(msg_template5)
            
        else:
            try:
                msg = msg_template1.format(group[0])
                send_mim_msg(group, msg=msg)
            except:
                continue
    '''       
     
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
