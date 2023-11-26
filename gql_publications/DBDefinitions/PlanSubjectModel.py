from .base import BaseModel
from .uuid import UUIDColumn

class PlanSubjectModel(BaseModel):
    """Spravuje data spojena s predmetem"""

    __tablename__ = "plan_subjects"

    id = UUIDColumn()