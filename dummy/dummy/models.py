from dummy.config import db, ma


class Rate(db.Model):
    __tablename__ = "rate"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    rate = db.Column(db.Integer)


class Result(db.Model):
    __tablename__ = "result"
    result_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    name = db.Column(db.String(32))
    points = db.Column(db.Integer)
    date = db.Column(db.Date)


class RateSchema(ma.ModelSchema):

    class Meta:
        model = Rate
        sqla_session = db.session


class ResultSchema(ma.ModelSchema):

    class Meta:
        model = Result
        sqla_session = db.session

