from prisma import models

models.User.create_partial("UserSchema", exclude_relational_fields=True)
