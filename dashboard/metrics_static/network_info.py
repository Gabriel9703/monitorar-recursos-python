from psutil import net_if_addrs, net_io_counters


class NetworkInfo:
    def __init__(self):
        self.__net_io_counters = net_io_counters()
        self.__net_if_addrs = net_if_addrs()

    def get_total_sent(self):
        return self.__net_io_counters.bytes_sent
    
    def get_total_recv(self):
        return self.__net_io_counters.bytes_recv    
    
    def get_total_sent_errors(self):
        return self.__net_io_counters.errout
    
    def get_total_recv_errors(self):
        return self.__net_io_counters.errin
    
    def get_total_dropped_in(self):
        return self.__net_io_counters.dropin
    
    def get_total_dropped_out(self):
        return self.__net_io_counters.dropout
    
    def get_total_packets_sent(self):
        return self.__net_io_counters.packets_sent
    
    def get_total_packets_recv(self):
        return self.__net_io_counters.packets_recv
    
    def get_interfaces(self):
        return self.__net_if_addrs
    