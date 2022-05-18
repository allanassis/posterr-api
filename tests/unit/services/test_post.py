from unittest.mock import patch, MagicMock
from unittest import TestCase
from posterr.services.post import Post, PostType

# TODO: Remove duplicated code and centralize in a method
class TestPost(TestCase):
    @patch("posterr.services.post.ConfigManager")
    def test_constructor_no_errors(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 100
        props = {
            "text":"text",
            "user_id": "user_id",
            "parent_id": "parend_id",
            }

        # act
        post = Post(**props)

        # assert
        self.assertIsInstance(post, Post)

    @patch("posterr.services.post.ConfigManager")
    def test_constructor_exceeding_text_limit(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 2
        props = {
            "text":"text",
            "user_id": "user_id",
            "parent_id": "parend_id",
            }

        # act / assert
        with self.assertRaises(ValueError):
            post = Post(**props)

    @patch("posterr.services.post.ConfigManager")
    def test_constructor_parent_id_is_none(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 5
        props = {
            "text":"text",
            "user_id": "user_id",
            }

        # act
        post = Post(**props)

        # assert
        self.assertRaises(AttributeError)
    
    @patch("posterr.services.post.ConfigManager")
    def test_constructor_type_is_none(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_int.return_value = 5
        props = {
            "text":"text",
            "user_id": "user_id",
            "parent_id": "parend_id",
            }

        # act
        post = Post(**props)

        # assert
        self.assertEqual(post.type, PostType.NORMAL.value)
    
    @patch("posterr.services.post.ConfigManager")
    def test_str(self, config_mock):
        # arrange
        instance = config_mock.return_value
        instance.config = MagicMock()
        instance.config.get_string.return_value = "%b %d, %Y"
        instance.config.get_int.return_value = 15
        props = {
            "text":"text",
            "user_id": "user_id",
            "parent_id": "parend_id",
            }
        # expected = 
        # act
        post = Post(**props)

        # assert
        self.assertIsInstance(str(post), str)    
    

        


