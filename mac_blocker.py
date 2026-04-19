# mac_blocker.py
# SDN Access Control using POX Controller
# Blocks unauthorized host (h3) using MAC-based filtering

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr
from pox.lib.util import dpidToStr

log = core.getLogger()

# MAC address of blocked host (h3)
BLOCKED_HOSTS = {
    EthAddr("00:00:00:00:00:03"),
}

# High priority so rules are not overridden
PRIORITY_BLOCK = 65535


def install_block_rules(connection):
    """
    Install OpenFlow rules to block traffic
    to and from unauthorized hosts.
    """
    for blocked_mac in BLOCKED_HOSTS:

        # Drop packets FROM blocked host
        msg = of.ofp_flow_mod()
        msg.priority = PRIORITY_BLOCK
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match = of.ofp_match()
        msg.match.dl_src = blocked_mac
        msg.actions = []  # No action = DROP
        connection.send(msg)
        log.info("[BLOCK] Dropping traffic FROM %s", blocked_mac)

        # Drop packets TO blocked host
        msg = of.ofp_flow_mod()
        msg.priority = PRIORITY_BLOCK
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match = of.ofp_match()
        msg.match.dl_dst = blocked_mac
        msg.actions = []  # No action = DROP
        connection.send(msg)
        log.info("[BLOCK] Dropping traffic TO %s", blocked_mac)

    log.info("Block rules successfully installed.")


def _handle_ConnectionUp(event):
    """
    Triggered when switch connects to controller.
    """
    log.info("Switch connected: %s", dpidToStr(event.dpid))
    install_block_rules(event.connection)


def launch():
    """
    Entry point for POX module.
    """
    log.info("mac_blocker module loaded.")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
