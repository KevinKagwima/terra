from Models.base_model import db, BaseModel, get_local_time
from Models.clinic import Clinic

class Medicine(BaseModel, db.Model):
  __tablename__ = "medicine"
  name = db.Column(db.String(200), nullable=False)
  price = db.Column(db.Integer(), default=0)
  prescription = db.relationship("PrescriptionDetails", backref="prescribed_medicine", lazy=True)
  inventory = db.relationship("Inventory", backref="inventory", lazy=True)

  def __repr__(self):
    return f"{self.name} - {self.price}"

class Inventory(BaseModel, db.Model):
  __tablename__ = "inventory"
  clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'))
  medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'))
  quantity = db.Column(db.Integer(), default=0)
  inventory_hostory = db.relationship("InventoryHistory", backref="inventory_history", lazy=True)

  def __repr__(self):
    return f"{self.clinic_id} - {self.quantity}"

class InventoryHistory(BaseModel, db.Model):
  __tablename__ = "inventory_history"
  inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
  stock_added = db.Column(db.Integer(), default=0)
  date_updated = db.Column(db.DateTime(), default=get_local_time())

  def __repr__(self):
    return f"{self.inventory_id} - {self.stock_added}"
