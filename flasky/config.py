import os
# app.config can stored  fram ,develop and procedure Configuration Variable


class Config:
    SSL_DISABLE = True
    # CSRF protect
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # after each request,auto commit mysql change
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # define email theme and sender address
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '984455045@qq.com'

    FLASKY_CURRENT_USER = 'DEFAULT'
    # email receiver address,put in environ to defend others see
    # you can set it in env shell,then run the program
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # debug mode
    DEBUG = True
    # QQ mail server settings
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    UPLOAD_FOLDER = "/static/uploads/"
    ALLOWED_EXTENSIONS = ['mp4']
    # email sender address and password
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # contact mysql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'mysql+pymysql://root:123456@localhost:3306/JIN?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/JIN?charset=utf8'


class ProductionConfig(Config):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    # debug mode
    DEBUG = True
    threaded = True
    host = '0.0.0.0'
    # QQ mail server settings
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    # email sender address and password
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # contact mysql,123456 = password,JIN= databaseName
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:123456@localhost:3306/JIN?charset=utf8'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # send errorMessage to administer
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}