"""create initial tables

Revision ID: 0001_create_initial_tables
Revises:
Create Date: 2026-07-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_create_initial_tables"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=True),
        sa.Column("middle_name", sa.String(length=50), nullable=True),
        sa.Column("last_name", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.Column("password_hash", sa.String(), nullable=True),
        sa.Column("phone", sa.String(length=15), nullable=True),
        sa.Column("profile_image", sa.String(), nullable=True),
        sa.Column("is_email_verified", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "pending_users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("middle_name", sa.String(length=50), nullable=True),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("otp_code", sa.String(length=6), nullable=False),
        sa.Column("otp_expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_pending_users_id", "pending_users", ["id"], unique=False)
    op.create_index("ix_pending_users_email", "pending_users", ["email"], unique=True)
    op.create_table(
        "posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column("media_type", sa.String(length=20), nullable=True),
        sa.Column("media_url", sa.String(), nullable=True),
        sa.Column("author_name", sa.String(length=100), nullable=True),
        sa.Column("author_type", sa.String(length=20), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "password_resets",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("otp_code", sa.String(length=6), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_used", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "saved_posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("user_id", "post_id", name="unique_saved_post"),
    )
    op.create_index("ix_saved_posts_id", "saved_posts", ["id"], unique=False)
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("subscriber_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("creator_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("subscriber_id", "creator_id", name="unique_subscription"),
    )
    op.create_index("ix_subscriptions_id", "subscriptions", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_subscriptions_id", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_index("ix_saved_posts_id", table_name="saved_posts")
    op.drop_table("saved_posts")
    op.drop_table("password_resets")
    op.drop_table("posts")
    op.drop_index("ix_pending_users_email", table_name="pending_users")
    op.drop_index("ix_pending_users_id", table_name="pending_users")
    op.drop_table("pending_users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("categories")
