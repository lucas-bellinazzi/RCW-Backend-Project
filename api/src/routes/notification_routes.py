from flask import Blueprint, request
from src.controllers.notification_controller import NotificationController


notification_bp = Blueprint("notification_bp", __name__)
notification_controller = NotificationController()


@notification_bp.route("/notifications", methods=["GET"])
def get_my_notifications():
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    return notification_controller.get_my_notifications(unread_only)


@notification_bp.route("/notifications/<string:notification_id>/read", methods=["POST"])
def mark_as_read(notification_id):
    return notification_controller.mark_as_read(notification_id)


@notification_bp.route("/notifications/read-all", methods=["POST"])
def mark_all_as_read():
    return notification_controller.mark_all_as_read()


@notification_bp.route("/notifications/<string:notification_id>", methods=["DELETE"])
def delete_notification(notification_id):
    return notification_controller.delete_notification(notification_id)
