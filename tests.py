import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User
# from models import DEFAULT_IMAGE_URL, User

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

TEST_URL = "https://upload.wikimedia.org/wikipedia/commons/4/4f/DandelionFlower.jpg"

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Tests route list_user for accessing the data base and listing all
        current users."""

        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_add_user_form(self):
        """Tests route show_add_user_form for rendering the add user form."""

        with app.test_client() as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html= resp.get_data(as_text=True)
            self.assertIn("<!--Comment for test_show_add_", html)

    def test_create_new_user(self):
        """Tests route create_new_user for data that is posted on the add
        new user form."""

        with app.test_client() as c:

            data = {
                "first_name": "test2_first",
                "last_name": "test2_last",
                "image_url": TEST_URL
            }
            resp = c.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test2_first", html)

    def test_process_edit(self):
        """Tests route process_edit for data that is posted on a cancel action
        and data that is posted on a save action."""

        with app.test_client() as c:
            canceled_data = {
                "first_name": "cancel_first",
                "last_name": "cancel_last",
                "image_url": TEST_URL,
                "action": "Cancel"
            }
            resp_to_cancel = c.post(
                f"/users/{self.user_id}/edit",
                data=canceled_data,
                follow_redirects=True
            )
            html_for_cancel = resp_to_cancel.get_data(as_text=True)
            self.assertEqual(resp_to_cancel.status_code, 200)
            self.assertIn("test1_first", html_for_cancel)
            self.assertNotIn("cancel_first", html_for_cancel)


            saved_data = {
                "first_name": "save_first",
                "last_name": "save_last",
                "image_url": TEST_URL,
                "action": "Save"
            }
            resp_to_save = c.post(
                f"/users/{self.user_id}/edit",
                data=saved_data,
                follow_redirects=True
            )
            html_for_save = resp_to_save.get_data(as_text=True)
            self.assertEqual(resp_to_save.status_code, 200)
            self.assertIn("save_first", html_for_save)
            self.assertNotIn("test1_first", html_for_save)

    def test_delete_user(self):
        """Tests functionality of delete_user route."""
        with app.test_client() as c:
            resp_to_delete = c.post(
                f"/users/{self.user_id}/delete",
                follow_redirects=True
            )
            html_for_delete = resp_to_delete.get_data(as_text=True)
            self.assertEqual(resp_to_delete.status_code, 200)
            self.assertNotIn("test1_first", html_for_delete)