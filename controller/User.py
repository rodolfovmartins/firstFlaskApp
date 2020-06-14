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

    def recovery(self, email):
        return ''

    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            user = self.user_model.get_user_by_id()
            res = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_created': user.date_created
            }
            status = 200
        except Exception as e:
            print(e)
            result = {}
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }