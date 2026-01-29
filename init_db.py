import os
import django
from django.conf import settings

def initialize_db():
    """Ensure database is initialized with migrations on app startup"""
    if not settings.CONFIGURED:
        django.setup()
    
    # Run migrations
    from django.core.management import call_command
    try:
        call_command('migrate', verbosity=0, interactive=False)
        print("✓ Database migrations completed")
    except Exception as e:
        print(f"⚠ Migration error: {e}")

if __name__ == '__main__':
    initialize_db()
