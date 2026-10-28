from sqlalchemy import text
from sqlalchemy.orm import Session
from typing_extensions import TypedDict


class UserProfile(TypedDict):
    id: int
    name: str | None
    email: str | None
    picture: str | None


class MemberRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_google_member(
        self,
        google_sub: str,
        email: str,
        name: str | None,
        picture: str | None,
        email_verified: bool,
    ) -> int:
        display_name = (name or "").strip() or email.partition("@")[0]
        with self.session.begin():
            self.session.execute(
                text(
                    """
                    SELECT pg_advisory_xact_lock(hashtextextended(:google_sub, 0))
                    """
                ),
                {"google_sub": google_sub},
            )
            member = self.session.execute(
                text(
                    """
                    SELECT user_id
                    FROM public.member
                    WHERE google_sub = :google_sub
                    FOR UPDATE
                    """
                ),
                {"google_sub": google_sub},
            ).mappings().one_or_none()

            if member is not None:
                user_id = member["user_id"]
                if user_id is None:
                    raise RuntimeError(
                        "Google member has no core user; apply the user/member migration"
                    )
                self.session.execute(
                    text(
                        """
                        UPDATE public.member
                        SET email = :email,
                            picture = :picture,
                            email_verified = :email_verified,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE google_sub = :google_sub
                        """
                    ),
                    {
                        "google_sub": google_sub,
                        "email": email,
                        "picture": picture,
                        "email_verified": email_verified,
                    },
                )
                self.session.execute(
                    text(
                        """
                        UPDATE public.users
                        SET display_name = :display_name
                        WHERE id = :user_id
                        """
                    ),
                    {"display_name": display_name, "user_id": user_id},
                )
            else:
                user_id = self.session.execute(
                    text(
                        """
                        INSERT INTO public.users (display_name, email, created_at)
                        VALUES (:display_name, :email, CURRENT_TIMESTAMP)
                        RETURNING id
                        """
                    ),
                    {"display_name": display_name, "email": email},
                ).scalar_one()
                self.session.execute(
                    text(
                        """
                        INSERT INTO public.member (
                            user_id, google_sub, email, name, picture, email_verified
                        )
                        VALUES (
                            :user_id, :google_sub, :email, :name, :picture,
                            :email_verified
                        )
                        """
                    ),
                    {
                        "user_id": user_id,
                        "google_sub": google_sub,
                        "email": email,
                        "name": name,
                        "picture": picture,
                        "email_verified": email_verified,
                    },
                )

        return user_id

    def get_user_profile_by_id(self, user_id: int) -> UserProfile | None:
        row = self.session.execute(
            text(
                """
                SELECT users.id, users.display_name AS name, member.email, member.picture
                FROM public.users AS users
                LEFT JOIN public.member AS member ON member.user_id = users.id
                WHERE users.id = :user_id
                """
            ),
            {"user_id": user_id},
        ).mappings().one_or_none()
        if row is None:
            return None

        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "picture": row["picture"],
        }
