""" Script to overwrite and delete user comments on reddit.com """

import sys
import argparse
import json
import praw


def authenticate_user(
    reddit_username, reddit_password, reddit_app_client_id, reddit_app_client_secret
):
    """Authenticates user with the PRAW library"""

    reddit = praw.Reddit(
        client_id=reddit_app_client_id,
        client_secret=reddit_app_client_secret,
        username=reddit_username,
        password=reddit_password,
        user_agent="comments-purger",
    )
    reddit.validate_on_submit = True

    return reddit.user.me() if reddit.user.me() == reddit_username else None


def delete_comments(redditor):
    """
    Deletes comments for a reddit user
    reddit: PRAW reddit user instance
    """

    for index, comment in enumerate(redditor.comments.new(limit=None)):
        print("Deleting comment {}".format(index))
        comment.edit("-")
        comment.delete()


def main():
    """Main function"""

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credential-file-path", type=str, help="Path to credential file"
    )
    parser.add_argument(
        "--2fa", action="store_true", help="Use two-factor authentication"
    )
    options = vars(parser.parse_args())

    # Authenticating user
    credentials = None
    print("Reading credentials")
    with open(options["credential_file_path"]) as credential_file:
        credentials = json.load(credential_file)
    if options["2fa"]:
        credentials["password"] += ':' + input("2FA token: ")

    print("Authenticating user")
    redditor = authenticate_user(
        credentials["username"],
        credentials["password"],
        credentials["client-id"],
        credentials["client-secret"],
    )
    print("Authentication successful")

    # Deleting comments
    print("Processing comments ...")
    delete_comments(redditor)
    print("Comment deletion completed!")


if __name__ == "__main__":
    main(sys.argv[1:])
