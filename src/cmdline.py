from argparse import ArgumentParser


def cmdline_parser():
    parser = ArgumentParser( description="bus décentralisé utilisant UDP/IP Multicast (UDPM) pour s'abonner et publier." )
    parser.add_argument('--impl', type=str, help='The implementation to use, between [basic and optimized]')
    parser.add_argument('--master'     , nargs='?', default=False      , help='The responsible of global topics publishing')
    parser.add_argument('--mcast-group', nargs='?', default='224.0.0.1', help='Multicast group (IP address)')
    parser.add_argument('--port'       , nargs='?', default=2416       , help='Port used to send and listen')
    return parser.parse_args()
