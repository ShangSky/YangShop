import time


def generate_order_num(user_id):
    order_num = "{}{}".format(time.strftime("%Y%m%d%H%M%S"), user_id)
    return order_num
