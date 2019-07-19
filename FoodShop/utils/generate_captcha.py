from captcha.image import ImageCaptcha
from random import randrange


class GenerateCaptcha(object):
    @staticmethod
    def __get_random_code(code_length):
        code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        code = ''
        for i in range(code_length):
            code += code_source[randrange(0, len(code_source) - 1)]
        return code

    def generate_image_captcha(self, code_length):
        code = self.__get_random_code(code_length)
        image = ImageCaptcha()
        data = image.generate(code)
        return code, data.read()
