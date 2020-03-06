from eve import Eve
from eve.auth import BasicAuth


class AppAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # TODO Add auth support
        pass


app = Eve()

if __name__ == '__main__':
    app.run()
