from .. import db

class Permission:
  FOLLOW = 1
  COMMENT = 2
  WRITE = 4
  MODERATE = 8
  ADMIN = 16

class Role(db.Model):
  __tablename__= 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True, index=True)
  users = db.relationship('User', backref='role')
  default = db.Column(db.Boolean, default=False, index=True)
  permissions = db.Column(db.Integer)

  def __init__(self, **kwargs):
    super(Role, self).__init__(**kwargs)
    if not self.permissions:
      self.permissions = 0

  def __repr__(self):
    return '<Role {}>'.format(self.name)

  def add_permissions(self, perm):
    if not self.has_permissions(perm):
      self.permissions += perm

  def remove_permissons(self, perm):
    if self.has_permissions(perm):
      self.permissions -= perm

  def reset_permissons(self):
    self.permissions = 0

  def has_permissions(self, perm):
    return self.permissions & perm == perm

  @staticmethod
  def insert_roles():
    roles = {
      'User':[Permission.COMMENT, Permission.FOLLOW, Permission.WRITE],
      'Moderator': [Permission.COMMENT, Permission.FOLLOW, Permission.WRITE, Permission.MODERATE],
      'Administrator': [Permission.COMMENT, Permission.FOLLOW, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
    }
    default_role = 'User'
    for r in roles:
      role = Role.query.filter_by(name=r).first()
      if not role:
        role = Role(name=r)
      role.reset_permissons()
      for perm in roles[r]:
        role.add_permissions(perm)
      role.default = role.name == default_role

      db.session.add(role)
      db.session.commit()
