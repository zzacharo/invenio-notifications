# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks related to notifications."""

from celery import shared_task

from .proxies import current_notifications_manager


@shared_task
def _send_notification_via_backend(notification, backend_id):
    """Task to send notification via backend."""
    current_notifications_manager.notify(notification, backend_id)


@shared_task
def broadcast_notification(notification):
    """Task to spawn single notification tasks."""
    for recipient in notification.recipients:
        for backend_payload in recipient.get("backends", []):
            _send_notification_via_backend.delay(
                notification, backend_payload.get("backend", "")
            )