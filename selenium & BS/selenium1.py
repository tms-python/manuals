from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

from feedback_app.models import (
    Recipient,
    Email,
    Feedback,
    Response,
    NoneAuthClientSession,
    ResponseAttachment,
    FeedbackAttachment,
    FeedbackStatus
)


class TestFromOrgToFeedbackResponseWithSelenium(StaticLiveServerTestCase):
    host = '127.0.0.1'
    port = 8025
    HOST = f'{host}:{port}'
    GROUP = 'ООО Ромашка'
    USERS = ['first_user', 'second_user']
    MAILS = ['agri88@yandex.ru', '2690736@gmail.com']
    SLEEP = 3
    ADMIN_USERNAME = 'admin'
    ADMIN_PASS = 'Agri07831505'

    def setUp(self):
        # modify_settings(DEBUG=True,CSRF_COOKIE_SECURE=True)

        self.driver = webdriver.Firefox()
        admin = User()
        admin.username = self.ADMIN_USERNAME
        admin.set_password(self.ADMIN_PASS)
        admin.is_superuser = True
        admin.is_active = True
        admin.is_staff = True
        admin.save()
        Group.objects.create(name='administrator')
        FeedbackStatus.objects.create(id=1, name='Отправлено')
        FeedbackStatus.objects.create(id=2, name='Принято к рассмотрению')
        FeedbackStatus.objects.create(id=3, name='Рассмотрено')
        super(TestFromOrgToFeedbackResponseWithSelenium, self).setUp()

    def test_full(self):
        # input('qwe')
        try:
            self.driver.get(f'http://{self.HOST}/admin')
            username = self.driver.find_element_by_id('id_username')
            username.send_keys(self.ADMIN_USERNAME)
            passwd = self.driver.find_element_by_id('id_password')
            passwd.send_keys(self.ADMIN_PASS)

            sub_btn = self.driver.find_element_by_class_name('submit-row').find_element_by_tag_name('input')
            sub_btn.click()

            add_recipient = self.driver.find_element_by_class_name('model-recipient').find_element_by_class_name(
                'addlink')
            add_recipient.click()

            new_recipient = self.driver.find_element_by_id('id_name').send_keys(f'{self.GROUP}')
            time.sleep(self.SLEEP)
            self.driver.find_element_by_name('_save').click()
            self.driver.get(f'http://{self.HOST}/admin')

            users = self.driver.find_element_by_class_name('model-user').find_element_by_class_name('addlink')
            users.click()
            new_user = self.driver.find_element_by_id('id_username').send_keys(self.USERS[0])
            new_user_pass = self.driver.find_element_by_id('id_password1').send_keys('zaq1@WSX')
            new_user_pass_confirm = self.driver.find_element_by_id('id_password2').send_keys('zaq1@WSX')
            time.sleep(self.SLEEP)
            save_and_continue = self.driver.find_element_by_name('_continue')
            save_and_continue.click()

            group = self.driver.find_element_by_name('groups_old').find_element_by_css_selector(
                f'[title="{self.GROUP}"]')
            group.click()
            add_group = self.driver.find_element_by_id('id_groups_add_link')
            add_group.click()
            group = self.driver.find_element_by_name('groups_old').find_element_by_css_selector(
                f'[title="administrator"]')
            group.click()
            add_group.click()
            time.sleep(self.SLEEP)
            self.driver.find_element_by_name('_save').click()
            self.driver.find_element_by_id('user-tools').find_elements_by_tag_name('a')[2].click()

            def auth_with_adm_user(URL, user):
                self.driver.get(f'http://{self.HOST}/{URL}')
                username = self.driver.find_element_by_id('id_username')
                username.send_keys(user)
                passwd = self.driver.find_element_by_id('id_password')
                passwd.send_keys('zaq1@WSX')
                sub_btn = self.driver.find_element_by_id('sub_btn')
                sub_btn.click()

            auth_with_adm_user('feedback/recipient_admin/', self.USERS[0])

            # create new user into ORG
            self.driver.find_element_by_id('create_user_button_id').click()
            self.driver.find_element_by_id('username').send_keys(self.USERS[1])
            self.driver.find_element_by_id('password').send_keys('zaq1@WSX')
            self.driver.find_element_by_id('email').send_keys('agri88@yandex.ru')
            self.driver.find_element_by_id('first_name').send_keys(self.USERS[1])
            self.driver.find_element_by_id('last_name').send_keys(self.USERS[1])
            self.driver.find_element_by_id('save_user_button_id').click()
            time.sleep(self.SLEEP)
            self.driver.switch_to_alert().accept()

            # add ORG emails
            for i, mail in enumerate(self.MAILS):
                self.driver.find_element_by_id('add_email_id').click()
                self.driver.find_element_by_id(f'mail{i}id').find_element_by_tag_name('span').click()
                email_input = self.driver.find_element_by_id(f'mail{i}id').find_element_by_tag_name('input')
                [email_input.send_keys(Keys.BACK_SPACE) for j in range(30)]
                email_input.send_keys(mail)
                email_input.send_keys(Keys.ESCAPE)
            # time.sleep(20)

            self.driver.get(f'http://{self.HOST}/user/logout/')
            # new feedback
            recipient = Recipient.objects.get(name=self.GROUP)
            recipient_feedback_link = recipient.feedback_for_recipient()
            print(f'http://{self.HOST}{recipient_feedback_link}')
            input('create feedback and press enter....')

            def make_feedback_response(feedback):
                print(feedback, feedback.content)
                auth_with_adm_user('feedback/recipient/', self.USERS[0])
                time.sleep(self.SLEEP)
                self.driver.find_element_by_id(f'feedback_sender_{feedback.id}').click()
                time.sleep(self.SLEEP)
                users_list = Select(self.driver.find_element_by_id('select_responsible_person_id'))

                responsible_user_id = User.objects.get(username=self.USERS[1])
                print(responsible_user_id)
                users_list.select_by_value(str(responsible_user_id.id))
                time.sleep(self.SLEEP)
                self.driver.find_element_by_id('confirm_btn_responsible_person_id').click()
                self.driver.get(f'http://{self.HOST}/user/logout/')

                auth_with_adm_user('feedback/recipient/', self.USERS[1])
                self.driver.find_element_by_id('on_pending_feedback_id___BV_tab_button__').click()
                time.sleep(self.SLEEP)
                self.driver.find_element_by_id(f'feedback_sender_{feedback.id}').click()
                time.sleep(self.SLEEP)
                self.driver.find_element_by_id('response_content_id').send_keys('Добрый ответ123')
                self.driver.find_element_by_id('file_attachment_id').send_keys('/home/agri/Documents/111.csv')
                self.driver.find_element_by_id('save_response_btn_id').click()
                time.sleep(self.SLEEP)
                self.driver.find_element_by_id('send_response_and_close_btn_id').click()
                self.driver.get(f'http://{self.HOST}/user/logout/')

            feedbacks = Feedback.objects.all().order_by('id')
            if len(feedbacks) == 2:
                for feedback in feedbacks:
                    make_feedback_response(feedback)
            elif len(feedbacks) == 1:
                make_feedback_response(feedbacks[0])

            self.driver.get(f'http://{self.HOST}/feedback/')
            self.driver.find_element_by_id('phone_number_id').send_keys('375339018001')
            self.driver.find_element_by_id('get_code_btn_id').click()
            time.sleep(self.SLEEP)
            verify_code = str(NoneAuthClientSession.objects.last().validate_code)
            self.driver.find_element_by_id('validate_code_id').send_keys(verify_code)
            self.driver.find_element_by_id('search_feedback_btn_id').click()
            input('press Enter....')
            self.driver.close()
        except Exception as e:
            print(e)

    def tearDown(self):
        super(TestFromOrgToFeedbackResponseWithSelenium, self).tearDown()
        try:
            input('enter for end')
            feedback = Feedback.objects.order_by('id').last()
            print(feedback)
            if feedback.content == 'Очень важное сообщение':
                response = Response.objects.get(feedback=feedback)
                print(response, response.content, sep='\n')
                for attachment in ResponseAttachment.objects.filter(response=response):
                    attachment.delete()
                time.sleep(1)
                response.delete()
                print('Response deleted')
                # print(response)
                # feedback.delete()
                # print('Feedback deleted')
        except Exception as e:
            print('recipient', e)
        time.sleep(2)
        try:
            feedback = Feedback.objects.order_by('id').last()
            print(feedback)
            if feedback.content == 'Очень важное сообщение':
                for attach in FeedbackAttachment.objects.filter(message=feedback):
                    attach.delete()
                time.sleep(1)
                feedback.delete()
                print('Feedback deleted')
        except Exception as e:
            print('recipient', e)
        try:
            Email.objects.get(email=self.MAILS[0]).delete()
            print('Email1 deleted')
        except Exception as e:
            print('recipient', e)
        try:
            Email.objects.get(email=self.MAILS[1]).delete()
            print('Email2 deleted')
        except Exception as e:
            print('recipient', e)
        try:
            Recipient.objects.get(name=self.GROUP).delete()
            print('recipient deleted')
        except Exception as e:
            print('recipient', e)
        try:
            Group.objects.get(name=self.GROUP).delete()
            print('group deleted')
        except Exception as e:
            print('group', e)
        try:
            User.objects.get(username=self.USERS[0]).delete()
            print('user1 deleted')
        except Exception as e:
            print('user1', e)
        try:
            User.objects.get(username=self.USERS[1]).delete()
            print('user2 deleted')
        except Exception as e:
            print('user2', e)

# class UserLoginTestCase(APITestCase):
#     user = None
#     # fixtures = ['Groups.json', 'Users.json']
#     def setUp(self):
#         group = Group.objects.create(name='administrator')
#         user = User.objects.create_user(
#             username='John',
#             email='johndoe@test.com',
#             password='john!doe',
#             first_name='John',
#             last_name='Doe',
#         )
#         user.groups.add(group)
#         user.save()
#         self.user = user
#
#
#     def test_user_serializer(self):
#         """
#         tests if all the nececarry  fields are in UserGroupSerializer serializer
#         """
#         self.assertIn('id', serializers.UserSerializer.Meta.fields)
#         self.assertIn('full_name', serializers.UserSerializer.Meta.fields)
#
#     def test_user_edit_serializer(self):
#
#         self.assertIn('id', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('username', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('first_name', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('last_name', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('email', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('groups', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('is_visible', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('groups_obj', serializers.UserEditSerializer.Meta.fields)
#         self.assertIn('is_active', serializers.UserEditSerializer.Meta.fields)
#
#     def test_user_edit_serializer_data(self):
#         user = serializers.UserEditSerializer(self.user).data
#
#         _id = user.get('id')
#         self.assertIsInstance(_id, int)
#         self.assertEqual(1, _id)
#
#         username = user.get('username')
#         self.assertIsInstance(username, str)
#         self.assertEqual('John', username)
#
#         first_name = user.get('first_name')
#         self.assertIsInstance(first_name, str)
#         self.assertEqual('John', first_name)
#
#         last_name = user.get('last_name')
#         self.assertIsInstance(last_name, str)
#         self.assertEqual('Doe', last_name)
#
#         email = user.get('email')
#         self.assertIsInstance(email, str)
#         self.assertEqual('johndoe@test.com', email)
#
#         groups = user.get('groups')
#         self.assertIsInstance(groups, list)
#         self.assertEqual([1], groups)
#
#         groups_obj = user.get('groups_obj')
#         self.assertIsInstance(groups_obj, list)
#         self.assertEqual(serializers.GroupSerializer(Group.objects.filter(id__in=groups), many=True).data,
#                          groups_obj)
#
#         is_visible = user.get('is_visible')
#         self.assertIsInstance(is_visible, bool)
#         self.assertEqual(True, is_visible)