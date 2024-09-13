from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    remember_token = Column(String)
    role = Column(Enum("superadmin", "admin", "operator", "customer", name="role"), default="customer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=False)
    

    profile = relationship("Profile", back_populates="user", uselist=False)
    property = relationship("Property", back_populates="user")
    

class Profile(Base):
    """Representasi tabel 'profile' di database."""

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    title = Column(Enum("mr", "mrs", name="title"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String)
    whatsapp = Column(String)
    address = Column(Text)
    province_id = Column(String, ForeignKey("regions.code"))
    district_id = Column(String, ForeignKey("regions.code"))
    city_id = Column(String, ForeignKey("regions.code"))
    village_id = Column(String, ForeignKey("regions.code"))
    gender = Column(Enum("man", "woman", name="gender"))
    birthday = Column(DateTime)
    avatar = Column(String)  
    remote_url = Column(String) # URL avatar
    social_media = Column(JSON) # Menambahkan kolom social_media dengan tipe data JSON
    company_name = Column(String(255))  # Menambahkan kolom company_name
    biodata_company = Column(Text) 
    jobdesk = Column(String(255))  # Menambahkan kolom biodata_company

    # Relasi ke tabel lain
    user = relationship("User", back_populates="profile")
    province = relationship("Region", foreign_keys=[province_id], lazy="joined", backref="profiles")
    district = relationship("Region", foreign_keys=[district_id], lazy="joined", backref="profile_districts")
    city = relationship("Region", foreign_keys=[city_id], lazy="joined", backref="profile_cities")
    village = relationship("Region", foreign_keys=[village_id], lazy="joined", backref="profile_villages")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name_category = Column(Enum("home", "warehouse", "apartement", "homeshop", "kavling", "office", name="name_category"), nullable=False)
    slug = Column(String)
    icon_url = Column(String(255))

    property = relationship("Property", back_populates="category")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey("users.id")) # foreign key user_id
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False, index=True)
    period = Column(Enum("onetime", "monthly", "yearly", "weekly", name="period"))
    # facility_id = Column(Integer, ForeignKey("facilities.property_id"))
    # specification_id = Column(Integer, ForeignKey("specifications.property_id"))
    address = Column(Text)
    province_id = Column(String, ForeignKey("regions.code"), index=True)
    district_id = Column(String, ForeignKey("regions.code"), index=True)
    city_id = Column(String, ForeignKey("regions.code"), index=True)
    village_id = Column(String, ForeignKey("regions.code"), index=True)
    coordinates = Column(String) #latitude, longitude
    nearby = Column(String)  
    #image_id = Column(Integer, ForeignKey("property_images.id"))  # Mengubah image menjadi foreign key
    ads = Column(Enum("sell", "rent", name="ads"), index=True)
    status = Column(Enum("active", "sold", "rented", "inactive", name="property_status"), index=True)
    views_count = Column(Integer, default=0)
    featured = Column(Boolean, default=False)
    meta_title = Column(String)
    meta_description = Column(Text)
    keywords = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="property")
    
    category = relationship("Category", back_populates="property")
    facility = relationship("Facility", back_populates="property", uselist=False)
    specification = relationship("Specification", back_populates="property", uselist=False)
    province = relationship("Region", foreign_keys=[province_id])
    district = relationship("Region", foreign_keys=[district_id])
    city = relationship("Region", foreign_keys=[city_id])
    village = relationship("Region", foreign_keys=[village_id])
   
    images = relationship("PropertyImage", back_populates="property")


class Region(Base):
    __tablename__ = "regions"
    code = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Enum("province", "district", "city", "village", name="region_level"))



class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), unique=True)
    certificate = Column(Enum("shm", "shgb", "shp", "shgu", "shmsrs", "sta", name="certificate"))
    electricity = Column(Integer)
    line_phone = Column(Enum("yes", "no", "progress", name="line_phone"))
    internet = Column(String)
    road_width = Column(String)
    water_source = Column(String)
    hook = Column(Enum("yes", "no", name="hook"))
    condition = Column(Enum("very_good", "good", "semi_good", "average", "not_good", "bad", "very_bad", name="condition"))
    security = Column(Enum("yes", "no", name="security"))
    wastafel = Column(Enum("yes", "no", name="wastafel"))

    property = relationship("Property", back_populates="facility")


class Specification(Base):
    __tablename__ = "specifications"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), unique=True)
    land_size = Column(Integer)
    building_size = Column(Integer)
    bedroom = Column(Integer)
    carport = Column(Integer)
    bathroom = Column(Integer)
    dining_room = Column(Integer)
    living_room = Column(Integer)
    floors = Column(Integer)

    property = relationship("Property", back_populates="specification")

class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    #property_id = Column(Integer)  # Kembalikan ke property_id
    #property_id = Column(Integer, ForeignKey("properties.image_id"))  # Kembalikan ke property_id
    property_id = Column(Integer, ForeignKey("properties.id"))
    image_url = Column(String)
    image_remote_url = Column(String)
    is_primary = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    property = relationship("Property", back_populates="images")