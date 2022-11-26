ALLOWED_MEAS_BANDWIDTH_ENUM = [6, 15, 25, 50, 75, 100]
NEIGH_CELL_CONFIG_DESC = [
    'Not all neighbour cells have the same MBSFN subframe allocation',
    'No MBSFN subframes are present in all neighbour cells',
    'The MBSFN subframe allocations of all neighbour cells are identical to or subsets of that in the serving cell',
    'Different UL/DL allocation in neighbouring cells for TDD compared to the serving cell',
]
Q_OFFSET_RANGE_ENUM = [-24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 8, 10,
                       12, 14, 16, 18, 20, 22, 24]


def get_rlcs(mac_layer):
    rlcs = mac_layer.get('rlc-lte', [])
    if not isinstance(rlcs, list):
        rlcs = [rlcs]
    return rlcs


def ul_nas_eps_from_rlc(rlc):
    ul = rlc.get('pdcp-lte').lte_rrc.UL_DCCH_Message_element.get('uL_DCCH_Message.message_tree').c1_tree
    ul = ul.ulInformationTransfer_element.criticalExtensions_tree.c1_tree.ulInformationTransfer_r8_element
    return ul.dedicatedInfoType_tree.dedicatedInfoNAS_tree.get('nas-eps')


def ul_nas_msg_container_from_rlc(rlc):
    return ul_nas_eps_from_rlc(rlc).get('NAS message container').get('emm.nas_msg_cont_tree')
