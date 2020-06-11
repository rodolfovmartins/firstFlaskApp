from flask_admin.contrib.sqla import ModelView
from config import app_active, app_config
from flask_admin import AdminIndexView, expose

config = app_config[app_active]

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home_admin.html', data={
            'username': 'Admin'
        })


class UserView(ModelView):

    column_labels = {
        'funcao': 'Função',
        'username': 'Nome do usuário',
        'email': 'E-mail',
        'date_created': 'Data de criação',
        'last_updated': 'Última atualização',
        'active': 'Ativo',
        'password': 'Senha'
    }

    column_descriptions = {
        'funcao': 'Função no painel administrativo',
        'username': 'Nome do usuário no sistema',
        'email': 'E-mail do usuário no sistema',
        'date_created': 'Data de criação do usuário no sistema',
        'last_updated': 'Última atualização desse usuário no sistema',
        'active': 'Estado ativo ou inativo no sistema',
        'password': 'Senha do usuário no sistema'
    }

    column_exclude_list = ['password', 'recovey_code']
    form_excluded_columns = ['last_updated', 'recovey_code']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    can_view_details = True
    can_set_page_size = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    column_editable_list = ['username', 'email', 'funcao', 'active']
    create_modal = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['username']
    column_default_sort = ('username', True)
    column_details_exclude_list = ['password', 'recovery_code']
    column_export_exclude_list = ['password', 'recovery_code']
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password

