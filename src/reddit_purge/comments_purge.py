"""Script to overwrite and delete user comments on reddit.com"""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime, timedelta

from asyncpraw import Reddit
from asyncpraw.models import Comment, Redditor

CONCURRENCY = 1


def non_negative_int(value: str) -> int:
    """argparse type for integer values that must not be negative"""

    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {ivalue}")
    return ivalue


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
    async with semaphore:
        await comment.edit("-")
        await comment.delete()
    print(f"Deleted comment {idx}")


async def delete_comments(redditor: Redditor, cutoff: float) -> None:
    """
    Deletes comments for a reddit user that are older than the cutoff timestamp
    reddit: PRAW reddit user instance
    cutoff: unix timestamp; comments created before it are deleted
    """

    semaphore = asyncio.Semaphore(CONCURRENCY)
    index = 0
    async with asyncio.TaskGroup() as tg:
        async for comment in redditor.comments.new(limit=None):
            if comment.created_utc >= cutoff:
                continue
            tg.create_task(
                delete_comment(idx=index, comment=comment, semaphore=semaphore)
            )
            index += 1
    print(f"Deleted {index} comment(s)")


async def async_main():
    """Main function"""

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credential-file-path",
        type=str,
        default=os.environ.get("CREDENTIAL_FILE_PATH"),
        help="Path to credential file (env: CREDENTIAL_FILE_PATH)",
    )
    parser.add_argument(
        "--days-to-retain",
        type=non_negative_int,
        default=0,
        help="Days of comment history to keep; older comments are deleted (default: 0)",
    )
    options = vars(parser.parse_args())
    cutoff = datetime.now(UTC) - timedelta(days=options["days_to_retain"])

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
        if options["days_to_retain"] == 0:
            print("Deleting all comments ...")
        else:
            print(
                "Deleting comments created before "
                f"{cutoff.strftime('%Y-%m-%d %H:%M UTC')} ..."
            )
        await delete_comments(redditor, cutoff.timestamp())
        print("Comment deletion completed!")
    finally:
        await reddit.close()


def main():
    asyncio.run(async_main())
