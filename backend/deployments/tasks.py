from celery import shared_task
from time import sleep
from clusters.models import Cluster
from deployments.models import Deployment

from django.db.models import Sum
from deployments.constants import DeploymentStatus
import datetime
from django.db import transaction
from clusters.handlers import ClusterHandler
from django.db.utils import OperationalError

RETRY_AFTER = 30


@shared_task(bind=True, max_retries=None)
def queue_deployment(self, deployment_id):
    """
    Processes a deployment by checking if cluster resources are available,
    then runs the deployment or requeues it if resources are insufficient.
    """
    try:
        deployment = Deployment.objects.get(id=deployment_id)
        with transaction.atomic():
            try:
                cluster = Cluster.objects.select_for_update(nowait=True).get(
                    id=deployment.cluster.id
                )  # Try to lock the cluster but don't wait

                if ClusterHandler().can_allocate_resources(cluster, deployment):
                    deployment.status = DeploymentStatus.RUNNING
                    deployment.started_at = datetime.datetime.now()
                    deployment.save()
                    cluster = ClusterHandler().allocate_resources(cluster, deployment)
                    cluster.save()  # Release lock on cluster
                    execute_deployment.delay(deployment_id)
                else:
                    # not enough resources, try later
                    print("not enough resources")
                    self.retry(countdown=RETRY_AFTER)
            except OperationalError:
                # couln't acquire lock, retry later
                print("Can't acquire lock")
                self.retry(countdown=RETRY_AFTER)
    except Deployment.DoesNotExist:
        print(f"Deployment {deployment_id} not found.")


@shared_task
def execute_deployment(deployment_id):
    try:
        deployment = Deployment.objects.get(id=deployment_id)
        sleep(deployment.duration)  # dummy deploying
        with transaction.atomic():
            cluster = Cluster.objects.select_for_update().get(
                id=deployment.cluster.id
            )  # locking this cluster
            deployment.status = DeploymentStatus.COMPLETED
            deployment.completed_at = datetime.datetime.now()
            deployment.save()
            cluster = ClusterHandler().free_resources(cluster, deployment)
            cluster.save()  # release lock on cluster
    except Deployment.DoesNotExist:
        print(f"Deployment {deployment_id} not found.")
    except Exception:
        deployment.status = DeploymentStatus.FAILED
        deployment.save()
