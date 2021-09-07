from hanspell import spell_checker
import re

class Preporcess:
    def __init__(self):
        self.checked = ''

    def spacing(self, review):
        try:
            spelled_sent = spell_checker.check(review)
            self.checked=spelled_sent.checked
        except Exception:
            self.checked=review
        
        return self.checked

    def dele(self, review):
        self.checked=review
        try:
            review = re.sub(pattern='([ㄱ-ㅎㅏ-ㅣ])+', repl='', string=review)
            review = re.sub(pattern='([-=+,#/\?:^$:;@*.\"~&%*!^_ㆍ])+', repl='', string=review)
            self.checked=review
        except Exception:
            self.checked=review
        return self.checked