from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_list = ['id', 'name', 'email']
    can_delete = False

