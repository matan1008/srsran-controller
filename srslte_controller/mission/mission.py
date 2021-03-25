class Mission:

    def __init__(self, epc, enb, network):
        """
        Create a new mission object.
        :param srslte_controller.mission.epc.Epc epc: Mission's EPC.
        :param srslte_controller.mission.enb.Enb enb: Mission's ENB.
        :param srslte_controller.mission.lte_network.LteNetwork network: Mission's network.
        """
        self.epc = epc
        self.enb = enb
        self._network = network

    def stop(self):
        """
        Stop the running mission.
        """
        self.enb.shutdown()
        self.epc.shutdown()
        self._network.shutdown()
