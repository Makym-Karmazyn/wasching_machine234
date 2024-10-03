"""база даних пралки"""
"""Спочатку я хотів зобити це як гру і через це додав базу даних з входом, але в мене час до четверга
і я зрозумів що не встигну недороблену гру видалив а вхід стало шкода і через це не став видаляти
на даний момент в ньому немає жодного сенсу, адже це просто додавання користувача в базу даних без жодного подальшого використання"""

from sqlalchemy import create_engine, false
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import String

engine = create_engine("sqlite:///app.db", echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    def createdb(self):
        Base.metadata.create_all(engine)

    def dropdb(self):
        Base.metadata.drop_all(engine)


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))

# db_1 = Base()
# db_1.dropdb()
# db_1.createdb()

"""Єдина функція реєстрації"""
def NewUser(username, password):
    with Session() as cursur:
        user_check = cursur.query(Users).filter_by(username=username).first()
        if user_check:
            if user_check.username == username and user_check.password == password:

                return "Congratulations, you have successfully log in your account"
            else:
                return "I'm sorry, but this name is prematurely used, or you input incorrect password.\nTry agin"
        else:
            new_user = Users(username=username, password=password)
            cursur.add(new_user)
            cursur.commit()
            return "Congratulations, you have successfully log in your account"
