from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

# Create your token generator here.


# Token Generator (for Activate Account)
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(
                user.is_active)
            )
