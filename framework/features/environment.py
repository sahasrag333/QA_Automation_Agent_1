from framework.utils.driver_factory import DriverFactory

def before_all(context):

    context.driver = DriverFactory.get_driver()


def after_all(context):

    DriverFactory.quit_driver()