from django.db.models import TextChoices


class DeploymentPriority(TextChoices):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DeploymentStatus(TextChoices):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


PRIORITY_MAPPING = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}
