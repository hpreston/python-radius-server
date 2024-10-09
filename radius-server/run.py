#!/usr/bin/python
from pyrad import dictionary, server
from RadiusServer import RadiusServer
import logging
from data import hosts

logging.basicConfig(
    filename="pyrad.log",
    level="DEBUG",
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)

if __name__ == "__main__":

    # create server and read dictionary
    srv = RadiusServer(dict=dictionary.Dictionary("dictionary"), coa_enabled=True)

    # add clients (address, secret, name)
    for host in hosts:
        srv.hosts[host] = server.RemoteHost(
            host, hosts[host]["key"].encode("utf-8"), hosts[host]["name"]
        )

    srv.BindToAddress("0.0.0.0")

    # start server
    srv.Run()
