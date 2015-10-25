# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from animals import model
from animals.controllers.secure import SecureController
from animals.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from animals.lib.base import BaseController
from animals.controllers.error import ErrorController
import logging
import transaction
from error_code import * 
from base import *

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the animals application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "animals"

    @expose('animals.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('animals.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('animals.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('animals.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)

    @expose('animals.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('animals.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    # @expose('animals.templates.login')
    # def login(self, came_from=lurl('/'), failure=None, login=''):
    #     """Start the user login."""
    #     if failure is not None:
    #         if failure == 'user-not-found':
    #             flash(_('User not found'), 'error')
    #         elif failure == 'invalid-password':
    #             flash(_('Invalid Password'), 'error')

    #     login_counter = request.environ.get('repoze.who.logins', 0)
    #     if failure is None and login_counter > 0:
    #         flash(_('Wrong credentials'), 'warning')

    #     return dict(page='login', login_counter=str(login_counter),
    #                 came_from=came_from, login=login)

    # @expose()
    # def post_login(self, came_from=lurl('/')):
    #     """
    #     Redirect the user to the initially requested page on successful
    #     authentication or redirect her back to the login page if login failed.

    #     """
    #     if not request.identity:
    #         login_counter = request.environ.get('repoze.who.logins', 0) + 1
    #         redirect('/login',
    #                  params=dict(came_from=came_from, __logins=login_counter))
    #     userid = request.identity['repoze.who.userid']
    #     flash(_('Welcome back, %s!') % userid)

    #     # Do not use tg.redirect with tg.url as it will add the mountpoint
    #     # of the application twice.
    #     return HTTPFound(location=came_from)

    # @expose()
    # def post_logout(self, came_from=lurl('/')):
    #     """
    #     Redirect the user to the initially requested page on logout and say
    #     goodbye as well.

    #     """
    #     flash(_('We hope to see you soon!'))
    #     return HTTPFound(location=came_from)

    @expose('json')
    def registe(self, user_name, password, email_address=''):
        '''
        '''
        # import ipdb;ipdb.set_trace()
        user = model.User()
        user.user_name = user_name
        user.password = password
        user.email_address = email_address

        # check registed user
        find_result = DBSession.query(model.User).filter_by(user_name=user_name).first()
        if find_result:
            return USER_EXIST

        try:
            DBSession.add(user)
            transaction.commit()
            return SUCCESS
        except Exception, e:
            transaction.abort()
            print 'error of registe: {}'.format(e)
            raise UNKNOW_ERROR

    @expose('json')
    def login(self, user_name, password):
        '''
        '''
        # import ipdb;ipdb.set_trace()

        # check registed user
        find_result = DBSession.query(model.User).filter_by(
            user_name=user_name).filter_by(password=password).first()
        if not find_result:
            return USER_PASSWORD_ERROR

        return LOGIN_SUCCESS

    @expose('json')
    def add_farm(self, **kw):
        '''
        '''
        # import ipdb;ipdb.set_trace()
        farm = model.Farm()
        # check registed user
        user_name = kw.get('user_name', '')
        find_result = DBSession.query(model.Farm).filter_by(user_name=user_name).first()
        if find_result:
            return USER_EXIST

        [setattr(farm, key, kw[key]) for key in FARM_KEYS if key in kw and kw[key] != '']

        try:
            DBSession.add(farm)
            transaction.commit()
            return SUCCESS
        except Exception, e:
            transaction.abort()
            print 'error of add_farm: {}'.format(e)
            return UNKNOW_ERROR

    @expose('json')
    def add_animals(self, **kw):
        '''
        '''
        # import ipdb;ipdb.set_trace()
        animals = model.FarmAnimals()

        [setattr(animals, key, kw[key]) for key in FARM_ANIMALS_KEYS if key in kw]
        [setattr(animals, key, int(kw[key])) for key in
            FARM_ANIMALS_INT_KEYS if key in kw and kw[key] != '']

        try:
            DBSession.add(animals)
            transaction.commit()
            return SUCCESS
        except Exception, e:
            transaction.abort()
            print 'error of add_farm: {}'.format(e)
            return UNKNOW_ERROR

    @expose('json')
    def add_user_animals(self, **kw):
        '''
        '''
        # import ipdb;ipdb.set_trace()
        animals = model.UserAnimals()

        [setattr(animals, key, int(kw[key])) for key in USER_ANIMALS_KEYS if key in kw]

        try:
            DBSession.add(animals)
            transaction.commit()
            return SUCCESS
        except Exception, e:
            transaction.abort()
            print 'error of add_farm: {}'.format(e)
            return UNKNOW_ERROR

    @expose('json')
    def user_animals(self, user_id):
        # import ipdb;ipdb.set_trace()

        result = {}
        result_list = []

        find_result = DBSession.query(model.UserAnimals, model.FarmAnimals).join(
            model.User, model.User.user_id==model.UserAnimals.user_id).join(
            model.FarmAnimals, model.FarmAnimals.animal_id==
            model.UserAnimals.animal_id)
        if user_id:
            find_result = find_result.filter(model.UserAnimals.user_id==user_id)

        read_all = find_result.all()
        if not read_all:
            return FIND_NOTHING
        
        def _trans_user_animals(target):
            '''
            translate target from object to dict
            '''
            result_list_dict = {}
            for key in USER_ANIMALS_KEYS:
                result_list_dict.update({key: getattr(target, key)})
                if key in ('createtime', 'updatetime'):
                    result_list_dict[key] = str(getattr(target, key))
            return result_list_dict
        
        def _trans_animals(target):
            '''
            translate target from object to dict
            '''
            result_list_dict = {}
            for key in FARM_ANIMALS_KEYS:
                result_list_dict.update({key: getattr(target, key)})
                if key in ('createtime', 'updatetime'):
                    result_list_dict[key] = str(getattr(target, key))
            return result_list_dict

        for res in read_all:
            trans_result = {}
            if res[0]:
                trans_one = _trans_user_animals(res[0])
                trans_result.update(trans_one)
            if res[1]:
                trans_two = _trans_animals(res[1])
                trans_result.update(trans_two)
            result_list.append(trans_result)

        result['result_list'] = result_list
        return result

    @expose('json')
    def farm_list(self, ):
        # import ipdb;ipdb.set_trace()

        result = {}
        result_list = []

        find_result = DBSession.query(model.Farm).all()
        if not find_result:
            return FIND_NOTHING
        
        def _trans(target):
            '''
            translate target from object to dict
            '''
            result_list_dict = {}
            for key in FARM_KEYS:
                result_list_dict.update({key: getattr(target, key)})
                if key in ('createtime', 'updatetime'):
                    result_list_dict[key] = str(getattr(target, key))
            return result_list_dict
        
        for res in find_result:
            trans_result = {}
            if res:
                trans_one = _trans(res)
                trans_result.update(trans_one)
            result_list.append(trans_result)

        result['result_list'] = result_list
        return result

    @expose('json')
    def farm_animals(self, farm_id=''):
        # import ipdb;ipdb.set_trace()
        result = {}
        result_list = []

        find_result = DBSession.query(model.FarmAnimals)
        if farm_id:
            find_result = find_result.filter_by(farm_id=farm_id)
        read_all = find_result.all()
        if not read_all:
            return FIND_NOTHING
        
        def _trans(target):
            '''
            translate target from object to dict
            '''
            result_list_dict = {}
            for key in FARM_ANIMALS_KEYS:
                result_list_dict.update({key: getattr(target, key)})
                if key in ('createtime', 'updatetime'):
                    result_list_dict[key] = str(getattr(target, key))
            return result_list_dict
        
        for res in read_all:
            trans_result = {}
            if res:
                trans_one = _trans(res)
                trans_result.update(trans_one)
            result_list.append(trans_result)

        result['result_list'] = result_list
        return result
