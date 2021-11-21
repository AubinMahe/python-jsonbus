from argparse import ArgumentParser


def cmdline_parser():
    parser = ArgumentParser( description="bus décentralisé utilisant UDP/IP Multicast (UDPM) pour s'abonner et publier." )
    parser.add_argument('--impl', type=str, help='The implementation to use, in [basic,master,random]')
    parser.add_argument('--master'     , nargs='?', default=False      , help='The responsible of global topics publishing')
    parser.add_argument('--observer'   , nargs='?', default=False      , help='True when this process is an observer')
    parser.add_argument('--mcast-group', nargs='?', default='224.1.2.3', help='Multicast group (IP address)')
    parser.add_argument('--ttl'        , nargs='?', default=10         , help='Time-To-Live des paquets multicast')
    parser.add_argument('--port'       , nargs='?', default=2416       , help='Port used to send and listen')
    return parser.parse_args()
