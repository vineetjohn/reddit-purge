"""Script to overwrite and delete user comments on reddit.com"""

import asyncio
import argparse
import json
from asyncpraw.models import Redditor, Comment
from asyncpraw import Reddit

CONCURRENCY = 3


async def authenticate(
    reddit_username, reddit_password, reddit_app_client_id, reddit_app_client_secret
) -> Reddit:
    """Authenticates user with the PRAW library"""

    reddit = Reddit(
        client_id=reddit_app_client_id,
        client_secret=reddit_app_client_secret,
        username=reddit_username,
        password=reddit_password,
        user_agent="comments-purger",
    )
    reddit.validate_on_submit = True
    return reddit


async def delete_comment(
    idx: int, comment: Comment, semaphore: asyncio.Semaphore
) -> None:
    print(f"Deleting comment {idx} ...")
    async with semaphore:
        await comment.edit("-")
        await comment.delete()
    print(f"Deleted comment {idx}")


async def delete_comments(redditor: Redditor) -> None:
    """
    Deletes comments for a reddit user
    reddit: PRAW reddit user instance
    """

    semaphore = asyncio.Semaphore(CONCURRENCY)
    async with asyncio.TaskGroup() as tg:
        index = 0
        async for comment in redditor.comments.new(limit=None):
            tg.create_task(
                delete_comment(idx=index, comment=comment, semaphore=semaphore)
            )
            index += 1


async def async_main():
    """Main function"""

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credential-file-path", type=str, help="Path to credential file"
    )
    options = vars(parser.parse_args())

    # Authenticating user
    credentials = None
    print("Reading credentials")
    with open(options["credential_file_path"]) as credential_file:
        credentials = json.load(credential_file)

    print("Authenticating user")
    reddit = await authenticate(
        credentials["username"],
        credentials["password"],
        credentials["client-id"],
        credentials["client-secret"],
    )

    try:
        redditor: Redditor = await reddit.user.me()
        if redditor is None:
            raise RuntimeError(f"Failed to authenticate as {credentials['username']}")
        print("Authentication successful")

        # Deleting comments
        print("Processing comments ...")
        await delete_comments(redditor)
        print("Comment deletion completed!")
    finally:
        await reddit.close()


def main():
    asyncio.run(async_main())
