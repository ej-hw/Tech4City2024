from sqlalchemy import create_engine, Integer, String, JSON, DateTime, select
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = 'analysis'

    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    topic = mapped_column(String)
    seed = mapped_column(String)
    message = mapped_column(String, nullable=False)
    results = mapped_column(JSON, nullable=False)
    reply = mapped_column(String)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

session = Session(engine)


def get_analyses():
    statement = select(Analysis).order_by(Analysis.created_at.asc())
    analyses = []

    for analysis in session.scalars(statement):
        analyses.append({
            "id": analysis.id,
            "topic": analysis.topic,
            "seed": analysis.seed,
            "message": analysis.message,
            "results": analysis.results,
            "reply": analysis.reply,
            "created_at": analysis.created_at
        })

    return analyses


def save_analysis(topic, seed, message, results, reply):
    analysis = Analysis(
        topic=topic,
        seed=seed,
        message=message,
        results=results,
        reply=reply
    )

    session.add(analysis)
    session.commit()

    return analysis


def delete_analysis(id):
    session.delete(session.get(Analysis, id))
    session.commit()
