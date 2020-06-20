from flask_admin.contrib.sqla import ModelView
from config import app_active, app_config
from flask_admin import AdminIndexView, expose
from model.User import User
from model.Category import Category
from model.Product import Product
from flask_login import current_user
from flask import redirect

config = app_config[app_active]

class HomeView(AdminIndexView):

    extra_css = [
        config.URL_MAIN + '/static/css/home.css',
        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
    ]

    @expose('/')
    def index(self):
        user_model = User()
        product_model = Product()
        category_model = Category()

        total_users = user_model.get_total_users()
        total_categories = category_model.get_total_categories()
        total_products = product_model.get_total_products()
        last_products = product_model.get_last_products()

        return self.render('home_admin.html', report={
            'total_users': 0 if not total_users else total_users[0],
            'total_categories': 0 if not total_categories else total_categories[0],
            'total_products': 0 if not total_products else total_products[0],
        }, last_products=last_products)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

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

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated


    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class RoleView(ModelView):
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class CategoryView(ModelView):
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class ProductView(ModelView):
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

        elif role == 4:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')