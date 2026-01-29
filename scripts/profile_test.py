from django.contrib.auth import get_user_model
from recipes.forms import UserProfileForm
from recipes.models import UserProfile

User = get_user_model()
u = User.objects.create_user("testprofileuser3","tp3@example.com","pass1234")
p, created = UserProfile.objects.get_or_create(user=u)
f = UserProfileForm(instance=p, data={"first_name":"T3","last_name":"P3","email":"tp3b@example.com","bio":"hi"}, user=u)
print("is_valid", f.is_valid())
print("errors", f.errors.as_json())
prof = f.save()
print("profile_id", prof.id, "user_first", u.first_name, "user_last", u.last_name, "user_email", u.email)
