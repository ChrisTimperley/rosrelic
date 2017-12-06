#!/usr/bin/env python3
import os
import sys
import requests
from typing import List, Tuple
from datetime import datetime


# Attempt to read the user's API token
if not os.path.exists('github.token'):
    print("ERROR: failed to find 'github.token' in current working directory.")
    sys.exit(1)

with open('github.token', 'r') as f:
    API_TOKEN = f.read().strip()


def tags_with_dates(repo_name: str,
                    repo_owner_name: str,
                    api_token: str = API_TOKEN
                    ) -> List[Tuple[str, str, datetime]]:
    """
    Returns an annotated list of all tagged releases for a given repository
    hosted on GitHub.

    Args:
        repo_name: The name of the repository on GitHub.
        repo_owner_name: The user or organisation that controls the given
            repository.

    Returns:
        An annotated list of release. Each release within the list is
        represented as a tuple of the form `(tag, sha, datetime)`, where
        `tag` is the name of the tag, `sha` is the hexsha of the commit
        associated with that tag, and `datetime` is the date/time that the
        commit associated with the tag was made.
    """

    # compute the URL for retrieving a list of releases for a given repo hosted
    # on GitHub
    # note: we use /tags since /releases only provides a list of "full"
    #   releases, which in many cases is an empty list.
    #   https://github.com/bcit-ci/CodeIgniter/issues/3421)
    endpoint = "repos/{}/{}/tags".format(repo_owner_name, repo_name)
    url = "https://api.github.com/{}".format(endpoint)
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {}'.format(api_token)}

    page = 0
    tags_with_commits : List[Tuple[str, str]] = []
    while True:
        page += 1
        params = {'page': page}
        r = requests.get(url, headers=headers, params=params)
        bfr = r.json()

        if not bfr:
            break

        if r.status_code == 403:
            raise Exception("Reached API usage limit!")

        for tag_info in bfr:
            name = tag_info['name']
            sha = tag_info['commit']['sha']
            tags_with_commits.append((name, sha))

    print(len(tags_with_commits))

    return []


def most_recent_tag_at_date(pkg_repo_name: str,
                            pkg_repo_owner_name: str,
                            dt: datetime = None
                            ) -> str:
    """
    Determines the most recent tagged release of a given project that was
    available at a given date and time. Note that the project must be
    hosted on GitHub for this method to work.

    Args:
        pkg_repo_name: The name of the Git repository used to host the
            package.
        pkg_repo_owner_name: The name of the user or organisation that owns
            the repository for the project. Note that the project must be
            hosted on GitHub.
        date: The date that should be used when determining the most recent
            tagged release.

    Returns:
        The name of the tagged release that was available at that moment in
        time.

    Raises:
        Exception: if no release was available at the given date.
            (TODO: add custom exception.)
    """
    # if no date/time is provided, use the current date/time
    if not dt:
        dt = datetime.today()

    dated_tags = tags_with_dates(pkg_repo_name, pkg_repo_owner_name)


def recreate_historical_rosinstall(pkg_repo_url: str,
                                   commit_sha: str
                                   ) -> str:
    """
    Produces a ROS install that estimates the state of a given project and its
    dependencies at a specific moment in time, corresponding to a given commit.


    Args:
        pkg_repo_url: The URL of the Git repository for the project that one
            wishes to recreate.
        commit_sha: The SHA of the commit that corresponds to the version of the
            Git repository that one wishes to recreate.

    Returns:
        A string containing the rosinstall file.
    """
    raise NotImplementedError


if __name__ == '__main__':
    most_recent_tag_at_date('php-src', 'php')
