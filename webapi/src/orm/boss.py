from webapi.index import db

class team(db.Document):
    team = db.StringField()
    turn = db.IntField()


class detail(db.Document):
    notice = db.StringField()
    teams = db.EmbeddedDocumentListField(team)


class state(db.Document):
    times = db.IntField(default=0)
    hp = db.StringField(default="max")


class Boss(db.Document):
    bossid = db.IntField()
    level = db.IntField()
    name = db.StringField()
    details = db.EmbeddedDocumentField(detail)
    status = db.EmbeddedDocumentField(state)


def AddorRestBoss(enemyID, name):
    level = enemyID.split('_')[0][-1]
    try:
        Boss.save(bossid=enemyID, name=name, level=level)
    except Exception as e:
        print("error: ", e)
        return False
    
    return True


def searchBoss(enemyID, level):
    boss = Boss.objects(bossid=enemyID).first()
    return boss