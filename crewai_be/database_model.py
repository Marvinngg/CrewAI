from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), unique=True, nullable=False)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class JobResult(db.Model):
    __tablename__ = 'job_results'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.job_id'), nullable=False)
    result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Text)
    goal = db.Column(db.Text)
    backstory = db.Column(db.Text)
    llm = db.Column(db.String(255))

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    tools = db.Column(db.Text)
    expected_output = db.Column(db.Text)

class Crew(db.Model):
    __tablename__ = 'crews'
    id = db.Column(db.Integer, primary_key=True)
    verbose = db.Column(db.Boolean, default=False)
    managellm = db.Column(db.String(255))

class CrewTask(db.Model):
    __tablename__ = 'crew_tasks'
    id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.Integer, db.ForeignKey('crews.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('crew_id', 'task_id', name='_crew_task_uc'),)

class CrewAgent(db.Model):
    __tablename__ = 'crew_agents'
    id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.Integer, db.ForeignKey('crews.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('crew_id', 'agent_id', name='_crew_agent_uc'),)