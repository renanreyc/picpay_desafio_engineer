from sqlalchemy import select

from src.models import User

def test_create_user(session):
    user =  User(username='test', 
                email='test@test.com',
                password='pass'
        )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'test@test.com')
    )
        

        
    assert result.id == 'id'
    assert result.username == 'test'