from slack import get_user_ids, send_mim_msg, send_pub_msg, get_conversations
import random
import time
# from db import db_init, db_add_stars, db_get_matches, db_close

if __name__ == '__main__':
    con_list = get_conversations()
    # print(con_list[2]['bot_id'])
    num = 0
    for con in con_list:
        num += 1
        if 'bot_id' in con:
            my_list = con
            print(my_list['reactions'])
            break
        print(str(num) + '번째 조회완료!')

    reactions = my_list['reactions']
    stars = []
    for reaction in reactions:
        stars.extend(reaction['users'])
    stars = list(set(stars))
    print(stars)
