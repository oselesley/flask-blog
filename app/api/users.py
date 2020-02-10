from . import api
from .. import db
from ..models.User import User
from flask import g, jsonify, request, current_app, url_for


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',  1, type=int)

    paginate = user.posts.paginate(page=page, per_page=int(current_app.config['FLASKY_POSTS_PER_PAGE']), error_out=False)
    posts = paginate.items

    prev = None
    if paginate.has_prev:
        prev = url_for('api.get_user_posts', id=user.id, page=page-1)
    next = None
    if paginate.has_next:
        next = url_for('api.get_user_posts', id=user.id, page=page+1)
    
    return jsonify({ 'posts': [post.to_json() for post in posts], 'prev_url': prev, 'next_url': next, 'count': paginate.total })

