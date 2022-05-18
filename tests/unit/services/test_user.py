from unittest.mock import patch, MagicMock
from unittest import TestCase
from posterr.services.user import User, UserValidationError

# TODO: Remove duplicated code and centralize in a method
class TestUser(TestCase):

    @patch("posterr.services.user.ConfigManager")
    def test_constructor_no_errors(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"name": "Malvin"}

        # act
        user = User(**props)

        # assert
        self.assertIsInstance(user, User)

    @patch("posterr.services.user.ConfigManager")
    def test_constructor_has_id(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        # act
        user = User(**props)

        # assert
        self.assertEqual(user._id, "some_id")

    
    @patch("posterr.services.user.ConfigManager")
    def test_constructor_name_exceeded_limit(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 3
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        # act / assert
        with self.assertRaises(UserValidationError):
            user = User(**props)

    @patch("posterr.services.user.ConfigManager")
    def test_constructor_invalid_name(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin+++!"}

        # act / assert
        with self.assertRaises(UserValidationError):
            user = User(**props)


    @patch("posterr.services.user.ConfigManager")
    def test_post(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}
        user = User(**props)

        post_dao = MagicMock()
        user_dao = MagicMock()
        db = MagicMock()
        cache = MagicMock()
        post = MagicMock()
        
        user.update = MagicMock()
        post.save = MagicMock(return_value="post_id")

        # act
        post_id = user.post(post, user_dao, post_dao, db, cache)

        # assert
        post.save.assert_called_once_with(post_dao, db)
        user.update.assert_called_once_with(user_dao, db, cache)
        self.assertListEqual(user.posts["list"], [post_id])
        self.assertEqual(user.posts["count"], 1)



    @patch("posterr.services.user.ConfigManager")
    def test_follow_your_self(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}
        user = User(**props)

        user_dao = MagicMock()
        db = MagicMock()
        cache =MagicMock()

        # act / assert
        with self.assertRaises(ValueError):
            user.follow("some_id", user_dao, db, cache)
    
    @patch("posterr.services.user.ConfigManager")
    def test_follow_user(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        user_instance = MagicMock()
        user_instance.update = MagicMock()
        User.get_by_id = MagicMock(return_value=user_instance)

        user = User(**props)
        user.update = MagicMock()

        user_dao = MagicMock()
        db = MagicMock()
        cache = MagicMock()

        # act
        user_id = user.follow("user_to_follow_id", user_dao, db, cache)

        # assert
        self.assertEqual(user_id, "some_id")
        self.assertEqual(User.get_by_id.call_count, 2)
        User.get_by_id.assert_any_call("some_id", user_dao, db, cache)
        User.get_by_id.assert_any_call("user_to_follow_id", user_dao, db, cache)
        self.assertEqual(user_instance.update.call_count, 2)

        
    @patch("posterr.services.user.ConfigManager")
    def test_unfollow_user(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        user_instance = MagicMock()
        user_instance.update = MagicMock()
        User.get_by_id = MagicMock(return_value=user_instance)

        user = User(**props)
        user.update = MagicMock()

        user_dao = MagicMock()
        db = MagicMock()
        cache = MagicMock()

        # act
        user_id = user.unfollow("user_to_follow_id", user_dao, db, cache)

        # assert
        self.assertEqual(user_id, "some_id")
        self.assertEqual(User.get_by_id.call_count, 2)
        User.get_by_id.assert_any_call("some_id", user_dao, db, cache)
        User.get_by_id.assert_any_call("user_to_follow_id", user_dao, db, cache)
        self.assertEqual(user_instance.update.call_count, 2)

    @patch("posterr.services.user.ConfigManager")
    def test_update(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        user = User(**props)

        user_dao = MagicMock()
        user_dao.update = MagicMock()
        db = MagicMock()
        cache = MagicMock()

        # act
        user.update(user_dao, db, cache)

        # assert
        user_dao.update.assert_called_once_with(user, db, cache)


    @patch("posterr.services.user.ConfigManager")
    def test_str(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 17
        instance.config.get_string.return_value = '\\w+'
        props = {"_id": "some_id", "name": "Malvin"}

        # act
        user = User(**props)

        # assert
        self.assertIsInstance(str(user), str)
