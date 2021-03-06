from application.src.models import Role
from flask_security.utils import hash_password

def build_sample_db(db, app, user_datastore):
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    with app.app_context():
        db.drop_all()
        db.create_all()

        user_role = Role(name='user')
        admin = Role(name='administrator')
        super_user_role = Role(name='superuser')

        db.session.add(user_role)
        db.session.add(admin)
        db.session.add(super_user_role)
        db.session.commit()

        user_datastore.create_user(
            first_name='Admin',
            email='admin',
            _password=hash_password('admin'),
            roles=[user_role, super_user_role, admin]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                _password=hash_password(tmp_pass),
                roles=[user_role, ]
            )
        db.session.commit()
    return
