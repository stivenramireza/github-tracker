from datetime import datetime

from src.entities.commit_entity import Commit


class CommitRepository:

    def insert(self, ctx: dict, commit: Commit) -> bool:
        conn, cursor = ctx

        query = """
            INSERT INTO commits (repo_name, commit_id, commit_message, author_username, author_email, payload, created_at, updated_at)
		    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        commit_dict = commit.__dict__
        del commit_dict['id']
        data = tuple(
            [
                value.isoformat() if isinstance(value, datetime) else value
                for value in commit_dict.values()
            ]
        )
        cursor.execute(query, data)
        conn.commit()

        return True

    def get_commits_by_author_email(self, ctx: tuple, email: str) -> list[Commit]:
        _, cursor = ctx

        query = """
            SELECT *
            FROM commits
            WHERE author_email = %s
        """

        data = (email,)
        cursor.execute(query, data)

        records = cursor.fetchall()

        commits: list[Commit] = []
        for record in records:
            (
                id,
                repo_name,
                commit_id,
                commit_message,
                author_username,
                author_email,
                payload,
                created_at,
                updated_at,
            ) = record
            commit = Commit(
                id=id,
                repo_name=repo_name,
                commit_id=commit_id,
                commit_message=commit_message,
                author_username=author_username,
                author_email=author_email,
                payload=payload,
                created_at=created_at.isoformat(),
                updated_at=updated_at.isoformat(),
            )
            commits.append(commit.__dict__)

        return commits
