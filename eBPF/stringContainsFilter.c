#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/udp.h>
#include <linux/limits.h>

#include<linux/tcp.h>	//Provides declarations for tcp header
#include<linux/ip.h>	//Provides declarations for ip header
#include<linux/socket.h>
#include<linux/inet.h>


#ifndef XDP_ACTION_MAX
#define XDP_ACTION_MAX (XDP_REDIRECT + 1)
#endif

#define CHAR_BIT 8

struct Row {
	unsigned char record [100];
};

BPF_ARRAY(filteredData, struct Row, 1000); // Map to store the data 
BPF_ARRAY(counter, int, 1); // Number of necessary packets

int udpstringContainsFilter(struct xdp_md *ctx) {

    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    uint32_t counter_key = 0; // Always index '0'
    char pattern[] = "test";

    unsigned int payload_size, i;
    struct ethhdr *eth = data;
    unsigned char *payload;
    struct udphdr *udp;
    struct iphdr *ip;

    if ((void *)eth + sizeof(*eth) > data_end){
        bpf_trace_printk("Ethernet header pointer exceeded the packet length\n");
        return XDP_DROP;
    }

    ip = data + sizeof(*eth);
    if ((void *)ip + sizeof(*ip) > data_end){
        bpf_trace_printk("IP header pointer exceeded the packet length\n");
        return XDP_DROP;
    }

    if (ip->protocol != IPPROTO_UDP){
        //bpf_trace_printk("Not a UDP packet\n");
        return XDP_PASS;
    }
    
    udp = (void *)ip + sizeof(*ip);

    if ((void *)udp + sizeof(*udp) > data_end){
        bpf_trace_printk("UDP header pointer exceeded the packet length\n");
        return XDP_DROP;
    }

    payload_size = ntohs(udp->len) - sizeof(*udp);
    payload_size = payload_size - 1;

    if (payload_size < sizeof(pattern) - 1) {
        bpf_trace_printk("Data string is shorter than pattern string");
        return XDP_DROP;
	}
    
    // Point to start of payload.
    payload = (unsigned char *)udp + sizeof(*udp);
    if ((void *)payload + payload_size > data_end){
        bpf_trace_printk("Payload pointer exceeded the packet length\n");
        return XDP_DROP;
    }
    
    char temp_cpy[sizeof(pattern)];
    bpf_probe_read_kernel(&temp_cpy,sizeof(pattern),payload);

    // Compare each byte, exit if a difference is found.
    for (i = 0; i < sizeof(pattern) - 1; i++) {
        if (temp_cpy[i] != pattern[i]) {
            bpf_trace_printk("Not a match");
            return XDP_DROP;
        }
    }
    
    // Find the row count and add the record to the map accordingly
    int *rowcount = counter.lookup(&counter_key);
    if(rowcount) {
        int rowcount_val = *rowcount;
        struct Row row = {};
        bpf_probe_read_kernel(&row.record,100,payload);
        filteredData.update(rowcount,&row);
        lock_xadd(rowcount, 1);
    }

    // Same payload, drop.
    return XDP_DROP;
}