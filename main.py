from fastapi import FastAPI
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker

app = FastAPI()

server_name = 'WWWEBLO'
database_name = 'people'

SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};SERVER=' + server_name +';DATABASE=' + database_name +';Trusted_Connection=yes;'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

'''
# Get all accounts
http GET http://127.0.0.1:8000/accounts

# Add a new account
http POST http://127.0.0.1:8000/accounts/add login="new_user" password="new_password"

# Update an account (replace <id> with an actual account ID)
http PUT http://127.0.0.1:8000/accounts/update/<id> login="updated_user" password="updated_password"

# Delete an account (replace <id> with an actual account ID)
http DELETE http://127.0.0.1:8000/accounts/delete/<id>

# Get all groups
http GET http://127.0.0.1:8000/groups

# Add a new group
http POST http://127.0.0.1:8000/groups/add name="new_group" creator=<id_of_creator>

# Update a group (replace <id> with an actual group ID)
http PUT http://127.0.0.1:8000/groups/update/<id> name="updated_group" creator=<id_of_creator>

# Delete a group (replace <id> with an actual group ID)
http DELETE http://127.0.0.1:8000/groups/delete/<id>

# Get all account groups
http GET http://127.0.0.1:8000/accountgroups

# Add a new account group
http POST http://127.0.0.1:8000/accountgroups/add id_account=<id_of_account> id_group=<id_of_group>

# Update an account group (replace <id> with an actual account group ID)
http PUT http://127.0.0.1:8000/accountgroups/update/<id> id_account=<new_id_of_account> id_group=<new_id_of_group>

# Delete an account group (replace <id> with an actual account group ID)
http DELETE http://127.0.0.1:8000/accountgroups/delete/<id>
'''

class Accounts(Base):
    __tablename__ = 'Accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))

    # Relationship with accounts_groups
    groups = relationship("AccountGroup", back_populates="account")

class Group(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    creator = Column(Integer, ForeignKey('Accounts.id'))

    accounts = relationship("AccountGroup", back_populates="group")

class AccountGroup(Base):
    __tablename__ = 'accounts_groups'

    id = Column(Integer, primary_key=True)
    id_account = Column(Integer, ForeignKey('Accounts.id'))
    id_group = Column(Integer, ForeignKey('Groups.id'))

    account = relationship("Accounts", back_populates="groups")
    group = relationship("Group", back_populates="accounts")

@app.get('/accounts')
def get_accounts():
    db = SessionLocal()
    accounts = db.query(Accounts).all()
    return {'accounts': [{'id': account.id, 'name': account.name, 'password': account.password} for account in accounts]}

@app.post('/accounts/add')
def add_account(data: dict):
    db = SessionLocal()
    new_account = Accounts(name=data['login'], password=data['password'])
    db.add(new_account)
    db.commit()
    return {'message': 'Account added successfully'}

@app.put('/accounts/update/{id}')
def update_account(id: int, data: dict):
    db = SessionLocal()
    account = db.query(Accounts).filter(Accounts.id == id).first()
    if account:
        account.name = data['login']
        account.password = data['password']
        db.commit()
        return {'message': 'Account updated successfully'}
    return {'message': 'Account not found'}

@app.delete('/accounts/delete/{id}')
def delete_account(id: int):
    db = SessionLocal()
    deleted = db.query(Accounts).filter(Accounts.id == id).delete()
    db.commit()
    if deleted:
        return {'message': 'Account deleted successfully'}
    return {'message': 'Account not found'}

# CRUD Groups

@app.get('/groups')
def get_groups():
    db = SessionLocal()
    groups = db.query(Group).all()
    return {'groups': [{'id': group.id, 'name': group.name, 'creator': group.creator} for group in groups]}

@app.post('/groups/add')
def add_group(data: dict):
    db = SessionLocal()
    new_group = Group(name=data['name'], creator=data['creator'])
    db.add(new_group)
    db.commit()
    return {'message': 'Group added successfully'}

@app.put('/groups/update/{id}')
def update_group(id: int, data: dict):
    db = SessionLocal()
    group = db.query(Group).filter(Group.id == id).first()
    if group:
        group.name = data['name']
        group.creator = data['creator']
        db.commit()
        return {'message': 'Group updated successfully'}
    return {'message': 'Group not found'}

@app.delete('/groups/delete/{id}')
def delete_group(id: int):
    db = SessionLocal()
    deleted = db.query(Group).filter(Group.id == id).delete()
    db.commit()
    if deleted:
        return {'message': 'Group deleted successfully'}
    return {'message': 'Group not found'}

# CRUD operations for AccountGroup

@app.get('/accountgroups')
def get_account_groups():
    db = SessionLocal()
    account_groups = db.query(AccountGroup).all()
    return {'account_groups': [{'id': ag.id, 'id_account': ag.id_account, 'id_group': ag.id_group} for ag in account_groups]}

@app.post('/accountgroups/add')
def add_account_group(data: dict):
    db = SessionLocal()
    new_account_group = AccountGroup(id_account=data['id_account'], id_group=data['id_group'])
    db.add(new_account_group)
    db.commit()
    return {'message': 'AccountGroup added successfully'}

@app.put('/accountgroups/update/{id}')
def update_account_group(id: int, data: dict):
    db = SessionLocal()
    account_group = db.query(AccountGroup).filter(AccountGroup.id == id).first()
    if account_group:
        account_group.id_account = data['id_account']
        account_group.id_group = data['id_group']
        db.commit()
        return {'message': 'AccountGroup updated successfully'}
    return {'message': 'AccountGroup not found'}

@app.delete('/accountgroups/delete/{id}')
def delete_account_group(id: int):
    db = SessionLocal()
    deleted = db.query(AccountGroup).filter(AccountGroup.id == id).delete()
    db.commit()
    if deleted:
        return {'message': 'AccountGroup deleted successfully'}
    return {'message': 'AccountGroup not found'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)