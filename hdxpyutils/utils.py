import boto3

session = None
logger = None

def create_session():
    session = boto3.session.Session()
    return session

def get_session():
    '''Singleton pattern for getting AWS session.'''
    global session
    if(session is None):
        session = create_session()
    return session