from . import api
from ..models.Post import Post
from ..models.User import User
from ..models.Role import Permission
from ..models.Comment import Comment
from .. import db
from flask import g, request, jsonify, make_response, url_for, current_app
from .decorators import permission_required
from .errors import forbidden

@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json(), 201, { 'Location': url_for('api.get_post', id=post.id) })

@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    paginate = Post.query.paginate(page=page, per_page=int(current_app.config['FLASKY_POSTS_PER_PAGE']), error_out=False)
    posts = paginate.items

    prev = None
    if paginate.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if paginate.has_next:
        next = url_for('api.get_posts', page=page+1)

    return jsonify({ 'posts': [post.to_json() for post in posts], 'prev_url': prev, 'next_url': next, 'count': paginate.total })

@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({ 'post': post.to_json() })

@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not g.current_user.is_admin or post.author != g.current_user:
        forbidden('Insufficient Permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json())

@api.route('/users/<int:id>')
def get_author(id):
    author = User.query.get_or_404(id)

    return jsonify(author.to_json())

@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)

    return jsonify(comment.to_json())


@api.route('/posts/<int:id>/comments/')
def get_comments(id):
    post = Post.query.get_or_404(id)
    comments = post.comments.all()
    return jsonify({ 'comments': [comment.to_json() for comment in comments] })


