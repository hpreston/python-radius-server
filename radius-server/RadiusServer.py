#!/usr/bin/python
from pyrad import packet, server
import logging
from platform_info import authentication_attributes, role_mapping
from data import users, hosts, authenticate_user

logging.basicConfig(
    filename="pyrad.log",
    level="DEBUG",
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)


class RadiusServer(server.Server):
    def _log_incoming_packet(self, type, pkt):
        username = pkt["User-Name"][0]
        print(f"Received an {type} request for user: [{username}]")
        logging.info(f"Received an {type} request for user: [{username}]")

        debug_msg = ""
        for attr in pkt.keys():
            debug_msg += f"{str(attr)}: {str(pkt[attr])} | "

        logging.debug(debug_msg)

    def HandleAuthPacket(self, pkt):
        username = pkt["User-Name"][0]
        pwd = pkt.PwDecrypt(pkt["User-Password"][0])
        host_ip = pkt["NAS-IP-Address"][0]

        device_type = hosts[host_ip]["device_type"]

        self._log_incoming_packet("authentication", pkt)

        reply = self.CreateReplyPacket(pkt, **{})

        authenticate_check = authenticate_user(username, pwd)
        print(f"Authentication Check: {authenticate_check}")
        logging.info(f"Authentication Check: {authenticate_check}")

        if authenticate_check == "Success":
            reply.code = packet.AccessAccept

            # Authorization and Role Assignment
            user_role = users[username]["role"]
            platform_role = role_mapping[device_type][user_role]
            print(f"Authorization Role: {device_type} | {platform_role}")
            logging.info(f"Authorization Role: {device_type} | {platform_role}")

            reply_attributes = authentication_attributes[hosts[host_ip]["device_type"]]
            for key, value in reply_attributes.items():
                reply.AddAttribute(key, value.format(role=platform_role))
        else:
            reply.code = packet.AccessReject
            if authenticate_check == "User not found":
                logging.debug(f"User: {username} not found in `network.yaml` file")

        logging.debug(reply)

        self.SendReplyPacket(pkt.fd, reply)

    def HandleAcctPacket(self, pkt):

        self._log_incoming_packet("accounting", pkt)

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):

        self._log_incoming_packet("coa", pkt)

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):

        self._log_incoming_packet("disconnect", pkt)

        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)
