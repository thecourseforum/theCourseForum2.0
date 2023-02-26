"""Application views."""

# See
# https://docs.djangoproject.com/en/3.0/topics/db/models/#organizing-models-in-a-package

from .auth import login, login_error, password_error, logout, collect_extra_info
from .ads import ads
from .index import index, privacy, terms, AboutView
from .browse import (browse, department, course_view_legacy, course_view,
                     course_instructor, instructor_view)
from .review import new_review, DeleteReview, upvote, downvote, edit_review
from .profile import profile, reviews, DeleteProfile
from .search import search
from .discord import post_message
from .qa import new_question
