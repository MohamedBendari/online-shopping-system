class User:
    def __init__(self,name,phone,email,gender,governorate,password,age,nationalID):
        self.name=name
        self.phone=phone
        self.email=email
        self.gender=gender
        self.governorate=governorate
        self.password=password
        self.age=age
        self.nationalID=nationalID
    def to_dict(self):
        return self.__dict__
    def from_dict(d):
        return User(d["name"],d["phone"],d["email"],d["gender"],d["governorate"],d["password"],d["age"],d["nationalID"])