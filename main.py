# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import redis
from redis import Sentinel
from redis.cluster import RedisCluster as Redis

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def connect_redis_cluster():
    rc = Redis(host='172.31.72.20', port=17342, password='redis', target_nodes=Redis.ALL_NODES)
    print(rc.get_nodes())
    rc.set('foo1', 'bar1')
    # target-nodes: the node that holds 'foo2's key slot
    rc.set('foo2', 'bar2')
    # target-nodes: the node that holds 'foo1's key slot
    print(rc.get('foo1'))
    rc.ping(target_nodes=Redis.PRIMARIES)
    keys = rc.keys(target_nodes=Redis.PRIMARIES)
    print(keys)


# Connection to the Sentinel Agents
def connect_sentinel():
    sentinel_list = [
        ('re1', 8001),
        ('re2', 8001)
    ]
    ssl_certfile="/Users/christianzumbiehl/.ssh/proxy-certificate.pem"
    ssl_keyfile = "/Users/christianzumbiehl/.ssh/proxy_key.pem"
    ssl_ca_certs = ssl_certfile

    # Without TLS
    #sentinel = Sentinel(sentinel_list, socket_timeout=5, password='redis', ssl=False)

    # This WORKS with TLS enabled
    #sentinel = Sentinel(sentinel_list, socket_timeout=5, password='redis', ssl=True, ssl_certfile=ssl_certfile, ssl_keyfile=ssl_keyfile,ssl_ca_certs=ssl_ca_certs,ssl_cert_reqs="required")

    #  THIS WORKS as well
    sentinel = Sentinel(sentinel_list, socket_timeout=5, password='redis',ssl=True,ssl_cert_reqs="none" )
    return sentinel


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print_hi('Sentinel Connect..')
    sentinel = connect_sentinel()
    # Connect to the DB "Stream"
    db_name = 'dbtest'
    r = sentinel.master_for(db_name, socket_timeout=0.5,)
    r.set('hello','world')
    value4 = r.get('hello')
    print(f'value = , {value4}')

    #print(f'Testing Cluster API')
    #connect_redis_cluster()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
