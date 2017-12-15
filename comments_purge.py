''' Script to overwrite and delete user comments on reddit.com '''

import sys
import argparse
import json
import praw


def authenticate_user(reddit_username, reddit_password,
                      reddit_app_client_id, reddit_app_client_secret):
    ''' Authenticates user with the PRAW library '''

    reddit = praw.Reddit(client_id=reddit_app_client_id,
                         client_secret=reddit_app_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent="comments-purger")

    return reddit if reddit.user.me() == reddit_username else None


def delete_comments(reddit):
    '''
    Deletes comments for a reddit user
    reddit: PRAW reddit instance
    '''
    # TODO: querying & deleting comments
    pass


def main(args):
    ''' Main function '''

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--credential-file-path', type=str,
                        help='Path to credential file')
    options = vars(parser.parse_args(args))

    # Authenticating user
    credentials = None
    with open(options['credential_file_path']) as credential_file:
        credentials = json.load(credential_file)
    reddit = authenticate_user(credentials['username'], credentials['password'],
                               credentials['client-id'], credentials['client-secret'])

    # Deleting comments
    delete_comments(reddit)

if __name__ == '__main__':
    main(sys.argv[1:])
