import asyncio
import os
import re
import unicodedata

import bcrypt as bcrypt
import markdown
import tornado
import tornado.web


def maybe_create_tables(db):
    with db.cursor() as cur:
        #cur.execute("DROP TABLE users ")
        cur.execute("CREATE TABLE IF NOT EXISTS users ("
                    "    id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                    "    email VARCHAR(100) NOT NULL UNIQUE,"
                    "    name VARCHAR(100) NOT NULL,"
                    "    hashed_password VARCHAR(100) NOT NULL,"
                    "    author int(5) NOT NULL DEFAULT 0"
                    ")")
        cur.execute("CREATE TABLE IF NOT EXISTS entries ("
                    "    id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                    "    author_id INT(5) NOT NULL REFERENCES authors(id),"
                    "    slug VARCHAR(100) NOT NULL UNIQUE,"
                    "    title VARCHAR(512) NOT NULL,"
                    "    markdown TEXT NOT NULL,"
                    "    html TEXT NOT NULL,"
                    "    published TIMESTAMP NOT NULL,"
                    "    updated TIMESTAMP NOT NULL"
                    ")")
    db.commit()


class NoResultError(BaseException):
    pass


class BaseHandler(tornado.web.RequestHandler):
    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc[0]] = row[desc[0]]
        return obj

    def execute(self, stmt, *args):
        """Execute a SQL statement.
        Must be called with ``await self.execute(...)``
        """
        with self.application.db.cursor() as cur:
            cur.execute(stmt, args)
        self.application.db.commit()

    def query(self, stmt, *args):
        """Query for a list of results.
        Typical usage::
            results = await self.query(...)
        Or::
            for row in await self.query(...)
        """
        with self.application.db.cursor() as cur:
            cur.execute(stmt, args)
            return [self.row_to_obj(row, cur) for row in cur.fetchall()]

    def queryone(self, stmt, *args):
        """Query for exactly one result.
        Raises NoResultError if there are no results, or ValueError if
        there are more than one.
        """
        results = self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    def prepare(self):
        # get_current_user cannot be a coroutine, so set
        # self.current_user in prepare instead.
        user_id = self.get_secure_cookie("blogdemo_user")
        if user_id:
            self.current_user = self.queryone("SELECT * FROM users WHERE id = %s",
                                              int(user_id))

    def any_users_exists(self):
        return bool(self.query("SELECT * FROM users LIMIT 1"))


class BlogComposeHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        user = self.current_user
        idarticle = self.get_argument("id", None)
        entry = None
        if idarticle:
            entry = self.queryone("SELECT * FROM entries WHERE id = %s", int(idarticle))
        self.render("blog\\compose.html", entry=entry, user=user)

    @tornado.web.authenticated
    async def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            try:
                entry = self.queryone("SELECT * FROM entries WHERE id = %s", int(id))
            except NoResultError:
                raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.execute(
                "UPDATE entries SET title = %s, markdown = %s, html = %s "
                "WHERE id = %s", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title)
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            slug = slug.encode("ascii", "ignore").decode("ascii")
            if not slug:
                slug = "entry"
            while True:
                e = self.query("SELECT * FROM entries WHERE slug = %s", slug)
                if not e:
                    break
                slug += "-2"
            self.execute(
                "INSERT INTO entries (author_id,title,slug,markdown,html,published,updated)"
                "VALUES (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)",
                self.current_user.id, title, slug, text, html)

        self.redirect("/blog/entry/" + slug)


class IndexHandler(BaseHandler):
    async def get(self):
        self.render("index.html")


class AuthLoginHandler(BaseHandler):
    async def get(self):
        get_arg = self.get_argument
        self.render("auth/login.html", error=None, get_arg=get_arg)

    async def post(self):
        try:
            user = self.queryone("SELECT * FROM users WHERE email = %s",
                                 self.get_argument("email"))
            print(user)
        except NoResultError:
            get_arg = self.get_argument
            self.render("auth/login.html", error="Email not found or bad password", get_arg=get_arg)
            return
        verified = await tornado.ioloop.IOLoop.current().run_in_executor(
            None, bcrypt.checkpw, tornado.escape.utf8(self.get_argument("password")),
            user.hashed_password.encode("utf-8"))
        if verified:
            self.set_secure_cookie("blogdemo_user", str(user.id))
            self.redirect(self.get_argument("next", "/"))
        else:
            get_arg = self.get_argument
            self.render("auth/login.html", error="Email not found or bad password", get_arg=get_arg)


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blogdemo_user")
        self.redirect(self.get_argument("next", "/"))


class AuthCreateHandler(BaseHandler):
    async def get(self):
        get_arg = self.get_argument
        self.render("auth/create_user.html", get_arg=get_arg)

    async def post(self):
        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
            None, bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt()
        )
        self.execute("INSERT INTO users (email, name, hashed_password) VALUES (%s, %s, %s)",
                     self.get_argument("email"), self.get_argument("name"),
                     tornado.escape.to_unicode(hashed_password))
        users = self.queryone("SELECT * FROM users WHERE email = %s", self.get_argument("email"))
        print(users)
        self.set_secure_cookie("blogdemo_user", str(users.id))
        self.redirect(self.get_argument("next", "/"))


class BlogHomeHandler(BaseHandler):
    async def get(self):
        entries = self.query("SELECT * FROM entries ORDER BY published DESC LIMIT 5")
        if not entries:
            self.redirect("/blog/compose")
            return
        self.render("blog\\index.html", entries=entries)


class BlogPostHandler(BaseHandler):
    async def get(self, slug):
        entry = self.queryone("SELECT * FROM entries WHERE slug = %s", slug)
        if not entry:
            raise tornado.web.HTTPError(404)

        self.render("blog\\entry.html", entry=entry)


class BotConnectHandler(BaseHandler):
    pass


class BotConfigureHandler(BaseHandler):
    pass


class BlogEntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("blog\\modules\\entry.html", entry=entry)


class FoWeb(tornado.web.Application):
    def __init__(self, bot, db):
        self.db = db
        maybe_create_tables(self.db)
        handlers = [
            (r"/", IndexHandler),
            (r"/blog/compose", BlogComposeHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/auth/create", AuthCreateHandler),
            (r"/blog", BlogHomeHandler),
            (r"/blog/entry/([^/]+)", BlogPostHandler),
            (r"/bot/connect", BotConnectHandler),
            (r"/bot/configure", BotConfigureHandler)
        ]
        settings = dict(
            website_title=u"FoBot",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            ui_modules={"BlogEntry": BlogEntryModule},
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        super(FoWeb, self).__init__(handlers, **settings)

    def get_task(self):
        return asyncio.ensure_future(tornado.ioloop.Future())
