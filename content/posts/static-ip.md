---
title: Achieving a Static IP Using a Free Proxy
date: 2019-12-23
---

At MIT, it's fairly trivial to get a static IP address (and subdomain under
`mit.edu`) for a specific MAC address connected to their wired Ethernet network
just by emailing the IT department. Having a static IP address is very
convenient for hosting websites and game servers, but more importantly it allows
easy access to my strong desktop computer from anywhere via [SSH][]. Sadly, my
living situation has changed and I no longer have a simple static IP address for
my desktop.

[SSH]: https://en.wikipedia.org/wiki/Secure_Shell

There are two concerns to be addressed here: a static public IP address and port
forwarding. Let's start with the former. I have recently moved into an apartment
where there is only one choice of internet service provider. They offer a
reasonable consumer plan of 100Mbit/s for $40/mo with a dynamic IP. Their
cheapest business plan with a static IP is 50Mbit/s for $100/mo. Not a great
deal.

Now, I could probably get by with purchasing a domain and reconfiguring DNS
records every time my dynamic IP changed. For some situations, your IP address
will only change when your ISP-provided modem has been disconnected for a
long-enough time period, like during a sustained power outage. For other
situations, like where your ISP employs [carrier grade NAT][cgnat], it may
happen more frequently. Ultimately, I don't know how frequently my public IP
address changes, and I'd prefer not to care.

[cgnat]: https://en.wikipedia.org/wiki/Carrier-grade_NAT

Now onto the second concern: port forwarding. Regardless of my ISP's network
situation, we have a wireless router in our apartment for connecting multiple
devices. Thus, even if I can reliably determine our public IP address, I must
configure our router to forward connections on certain ports to my computer. I
don't control this router, and I'd prefer not to have to repeatedly badger my
roommate whenever I want to test out new services. If my ISP did employ another
layer of NAT, then this wouldn't help anyway.

Both of these concerns can be addressed simultaneously using a [proxy][] and SSH
reverse port forwarding. 

[proxy]: https://en.wikipedia.org/wiki/Proxy_server

A commonly used flag of `ssh` is `-L`, which listens on a port of the local
machine and forwards traffic as if it originated from the remote machine. One
can also use the `-R` flag to do the opposite: to listen on the remote machine
and forward traffic as if it originated on the local machine.

First we will need a proxy server. You can use any host, but Google appears to
be the only major cloud provider offering an indefinite free VM at this
time[^free]. You'll have to search for another website to describe the in-depth
steps for setting up an `f1-micro` instance on Google's cloud.

[^free]: Google lists the f1-micro under their _Always Free_ tier
    [here][gcp4ever]. [Azure][azure12] and [AWS][aws12] both seem limited to 12
    months.

[gcp4ever]: https://cloud.google.com/free/docs/gcp-free-tier#always-free-usage-limits
[azure12]: https://azure.microsoft.com/en-us/free/free-account-faq/
[aws12]: https://aws.amazon.com/free/

The basic steps for any cloud provider are as follows:

1. Create the tiniest uninterruptible VM possible
2. Add a small hard drive if necessary
3. Select a linux distribution you're familiar with
4. Configure an SSH key
5. Configure the network rules (see below)

You have a choice when configuring network rules. If you use the server-optimized
version of Ubuntu chosen by most providers, it will already come with a firewall
that will block all ports besides ssh[^block]. This is separate from your providers
network rules, which can also block traffic destined for your VM. I would
recommend setting your cloud provider's network rules to accept traffic from all
IP addresses destined to any port. Then you only have to mess with the software
firewall[^around].

[^block]: <https://cloud.google.com/container-optimized-os/docs/how-to/firewall>
[^around]: You could chose the other way around: to set the software firewall to
    accept all traffic and to then filter things using your provider's network
    firewall. Google's web interface is terribly slow so I have not chosen this.
    One could also just set both firewalls to accept all traffic. Probably not a
    good idea.

Now you can launch the VM. It will be given a static IP address that will last
until the VM is terminated. Given the reliability of modern cloud data centers,
that means you now effectively have a permanent static IP.

# Setting Up a Specific Port

Say you want to run a web server on port `80`. First you need to set up the
proxy VM. This involves two things: opening the port in the software firewall
and also set up permissions for listening on that port. For Linux, a process
requires root privileges, or more specifically the `CAP_NET_BIND_SERVICE`
capability, to listen to a port below `1024`. I went with just logging in as
root[^easy], but in theory you can use the `setcap` utility on `/usr/sbin/sshd`
instead.

[^easy]: Only because I did not pay attention to the capability aspect when I first encountered this issue.

In order to log in as root, on my VM I ran:
```bash
sudo mkdir /root/.ssh/
sudo cp ~/.ssh/authorized_keys /root/.ssh/authorized_keys
```

You may also want to double check that your `/etc/ssh/sshd_config` lists
`PermitRootLogin` as `prohibit-password`.

Now you should open the port on your VM:
```bash
sudo iptables -w -A INPUT -p tcp --dport 80 -j ACCEPT
```

Now on your server in your local network, run the following:
```bash
ssh -N -R "*:80:localhost:80" root@your.vm.ip.here
```
Remove the `root@` portion of the destination IP address if you chose to use the `CAP_NET_BIND_SERVICE` capability.

The `-N` flag says that SSH doesn't need to run a command on the destination; it
will remain connected indefinitely. The syntax of the `-R` flag is `-R
[bind_address:]port:host:hostport`. The `bind_address` of `*` means listen on
all network interfaces, the `port` is the port to listen to on the proxy VM, and
the `host` and `hostport` are the destination of the traffic once it has been
forwarded back to your local server. You can use the `-R` flag multiple times to
listen on multiple ports simultaneously.

For a basic attempt at reliability in the face of network interruptions, I wrap that command in this small script:
```bash
#!/bin/bash
while true; do
  echo connecting
  ssh -N -R "*:80:localhost:80" root@your.vm.ip.here
  wait 3
done
```

Realistically, this should probably be a systemd service, but that's for another day.

# Forwarding SSH

For the time being, I mostly want to connect to my server for SSH. The easiest
option is to forward a port like `8192` on the proxy VM to port `22` on my local
server. Then I can simply add a small entry to `~/.ssh/config` and never worry about ports again:
```text
Host MyServer
    HostName my.vm.ip.here
    Port 8192
```

Now I can log in simply using `ssh MyServer`. The slightly more roundabout way
of achieving this is to make port `22` of the proxy forward to port `22` on my
server[^actual]. This requires first changing the what port the `sshd` running
on the proxy will listen to. I've chosen to make port `23` log in to the actual
VM whereas port `22` gets forwarded to my server.

[^actual]: This is what I actually use because I wanted to allow somone easy
    access to my desktop and I wanted it to be as convenient as possible.

First, open port `23` with `sudo iptables -w -A INPUT -p tcp --dport 23 -j
ACCEPT`. Then add `Port 23` to `/etc/ssh/sshd_config` and run `sudo service ssh
restart`. Finally, change how you invoke the ssh reverse port forwarding as so:

```bash
ssh -N -R "*:22:localhost:22" root@your.vm.ip.here -p 23
```

This will drive `ssh` a little crazy because it detects that it connected to a
different computer than expected. I suppose this is quite literally a
[man-in-the-middle attack][mitm], which `ssh` tries to prevent. You'll have to remove a
few lines from `~/.ssh/known_hosts` to quell things.

[mitm]: https://en.wikipedia.org/wiki/Man-in-the-middle_attack
