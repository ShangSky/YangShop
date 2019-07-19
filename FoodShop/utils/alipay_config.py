from alipay import AliPay
from FoodShop.settings import app_private_key_path, alipay_public_key_path, notify_url

alipay = AliPay(
    appid="",  # 应用id
    app_notify_url=notify_url,  # 默认回调url
    app_private_key_path=app_private_key_path,
    alipay_public_key_path=alipay_public_key_path,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=True  # 默认False
)
