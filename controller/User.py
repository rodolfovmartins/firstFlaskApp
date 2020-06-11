from model.User import User


class UserController:

    def __init__(self):
        self.user_model = User()

    def login(self, email, password):
        self.user_model.email = email
        user = self.user_model.get_user_by_email()

        if user is not None:
            res = self.user_model.verify_password(password, user.password)

            if res:
                return user
            else:
                return {}

        return {}

    def recovery(email):
        return ''