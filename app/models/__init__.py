<<<<<<< HEAD
from app.models.user import User, Role
from app.models.profile import Profile
from .article import Article  
=======
# Import order matters - put simple models first
from .user import User
from .profile import Profile
>>>>>>> 559d8bebe8bae22b33178d06e50b96e739d1860f
from .subscription_plan import SubscriptionPlan
from .article import Article

# Import more complex models last
from .category import Category, Subcategory
from .corporate import Corporate
from .resources import Resources