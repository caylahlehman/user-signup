import webapp2
import re
import cgi

page_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Signup</title>
    </head>
    <body>
        <h1>
            Signup
        </h1>
"""

page_footer = """
    </body>
    </html>
"""

form = """<form method = "post">
    <label>
        Username
        <input type = "text" name = "username" value = "%(username)s">
    </label>
    <span style = "color: red">%(err_1)s</span>
    <br>
    <label>
        Password
        <input type = "password" name = "password">
    </label>
    <span style = "color: red">%(err_2)s</span>
    <br>
    <label>
        Verify Password
        <input type = "password" name = "verify">
    </label>
    <span style = "color: red">%(err_3)s</span>
    <br>
    <label>
        Email (optional)
        <input type = "text" name = "email" value = "%(email)s">
    </label>
    <span style = "color: red">%(err_4)s</span>
    <br>
    <input type = "submit">
</form>"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username = "", err_1 = "", err_2 = "", err_3 = "", email = "", err_4 = ""):
        self.response.write((page_header) + (form % {"username":(cgi.escape(username, quote = True)), "err_1":(cgi.escape(err_1, quote = True)), "err_2":(cgi.escape(err_2, quote = True)), "err_3":(cgi.escape(err_3, quote = True)), "email":(cgi.escape(email, quote = True)), "err_4":(cgi.escape(err_4, quote = True))}) + page_footer)

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return PASS_RE.match(password)

    def valid_verify(self, password,verify):
        if password == verify:
            return True
        else:
            return False

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]$")
        if email == "" or EMAIL_RE.match(email):
            return True
        else:
            return False

    def get(self):
        self.write_form("","","","","","")

    def post(self):
        valid_username = self.valid_username(self.request.get("username"))
        valid_password = self.valid_password(self.request.get("password"))
        valid_verify = self.valid_verify(self.request.get("password"),self.request.get("verify"))
        valid_email = self.valid_email(self.request.get("email"))

        if (valid_username and valid_password and valid_verify and valid_email):
            username = self.request.get("username")
            self.redirect("/welcome?username=" + username)

        else:
            if valid_username:
                username = self.request.get("username")
                err_1 = ""
            else:
                username = ""
                err_1 = "The username is not valid."
            if not valid_password:
                err_2 = "The password is not valid."
            else:
                err_2 = ""
            if not valid_verify:
                err_3 = "The passwords do not match."
            else:
                err_3 = ""
            if valid_email:
                email = self.request.get("email")
                err_4 = ""
            else:
                email = ""
                err_4 = "The email is not valid."

            self.write_form(username, err_1, err_2, err_3, email, err_4)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        welcome_header = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Welcome</title>
            </head>
            <body>"""

        username = self.request.get("username")
        esc_username = (cgi.escape(username, quote = True))
        welcome = "Welcome, " + esc_username + "!"
        content = welcome_header + "<h1>" + welcome + "</h1>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
    ], debug = True)
