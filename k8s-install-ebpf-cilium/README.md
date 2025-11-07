# Kubernetes HA Cluster with eBPF/Cilium

Automated installation of a highly available Kubernetes cluster using Cilium eBPF for networking without IPVS and iptables.

[![Ansible](https://img.shields.io/badge/Ansible-2.9+-green.svg)](https://www.ansible.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34.1-blue.svg)](https://kubernetes.io/)
[![Cilium](https://img.shields.io/badge/Cilium-1.18.3-orange.svg)](https://cilium.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Author:** Sergey Rytsev

---

## 🚀 Quick Start

### 1. Configure Node IPs

**IMPORTANT:** Before starting, you must configure your node IP addresses in two files:

**Step 1:** Edit `group_vars/all.yml` and replace the placeholder IPs with your actual node IP addresses:

```yaml
k8s_master_1_ip: "YOUR_MASTER_1_IP"  # Replace with your first master node IP
k8s_master_2_ip: "YOUR_MASTER_2_IP"  # Replace with your second master node IP
k8s_master_3_ip: "YOUR_MASTER_3_IP"  # Replace with your third master node IP
```

**Step 2:** Edit `inventory/inventory.yml` and replace the placeholder IPs with the same IP addresses:

```yaml
k8s-master-1:
  ansible_host: "YOUR_MASTER_1_IP"  # Replace with your first master node IP
  node_ip: "YOUR_MASTER_1_IP"       # Replace with your first master node IP
k8s-master-2:
  ansible_host: "YOUR_MASTER_2_IP"  # Replace with your second master node IP
  node_ip: "YOUR_MASTER_2_IP"       # Replace with your second master node IP
k8s-master-3:
  ansible_host: "YOUR_MASTER_3_IP"  # Replace with your third master node IP
  node_ip: "YOUR_MASTER_3_IP"       # Replace with your third master node IP
```

**Note:** IP addresses in both files must match exactly. The IPs must be publicly accessible or reachable from your Ansible control node.

### 2. Verify Connection

```bash
cd k8s-install-ebpf-cilium
ansible all -m ping
```

### 3. Run Installation

```bash
ansible-playbook playbooks/site.yml
```

Installation takes approximately 5-10 minutes. All components will be installed automatically.

---

## ✨ Key Features

- ✅ **eBPF-based networking** - Cilium uses eBPF instead of traditional iptables/IPVS
- ✅ **kube-proxy replacement** - Cilium completely replaces kube-proxy
- ✅ **High Availability** - 3 control-plane nodes with etcd in HA mode
- ✅ **Gateway API** - Support for modern Gateway API for ingress
- ✅ **LoadBalancer** - Cilium LoadBalancer IP Pool for L2/L3 load balancing
- ✅ **Idempotency** - Playbooks can be run multiple times without issues
- ✅ **Best Practices 2025** - Compliance with modern Ansible standards

---

## 🏗️ Architecture

### Networking Stack

```
Kubernetes Cluster (HA)
    │
    ├── 3x Control Plane Nodes (etcd HA)
    │
    └── Cilium eBPF Networking
        ├── kube-proxy: Disabled (replaced by Cilium)
        ├── iptables: Not used
        ├── IPVS: Not used
        └── eBPF: Used for all networking logic
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|--------|
| **Kubernetes** | kubeadm | 1.34.1 |
| **CNI** | Cilium with eBPF | 1.18.3 |
| **Container Runtime** | containerd | 2.1.4 |
| **Gateway API** | CRDs | v1.3.0 |
| **CoreDNS** | Auto-scaling | Per node |

---

## 📁 Project Structure

```
k8s-install-ebpf-cilium/
├── ansible.cfg              # Ansible configuration
├── .ansible-lint            # ansible-lint configuration
├── README.md                # This documentation
├── requirements.yml         # Ansible dependencies
│
├── inventory/
│   └── inventory.yml       # Inventory file (node IP addresses)
│
├── group_vars/
│   └── all.yml             # ⭐ MAIN CONFIGURATION FILE
│                           #    All IPs, versions, and settings here
│
└── playbooks/
    ├── site.yml            # Full installation (all stages)
    ├── 00-check-system.yml # System requirements check
    ├── 01-prepare-nodes.yml # Node preparation
    ├── 02-init-cluster.yml  # First master initialization
    ├── 03-join-masters.yml  # Join remaining masters
    ├── 04-install-gateway-api.yml # Gateway API installation
    ├── 05-install-cilium.yml      # Cilium CNI installation
    ├── 06-configure-cilium-lb.yml # LoadBalancer configuration
    ├── 07-configure-gateway.yml   # Gateway configuration
    ├── 08-configure-node-roles.yml # Node roles configuration
    └── 09-install-coredns.yml     # CoreDNS installation
│
└── roles/
    ├── check-system/        # System check
    ├── prepare-nodes/      # Node preparation
    ├── init-cluster/        # Cluster initialization
    ├── join-masters/        # Master node joining
    ├── install-gateway-api/ # Gateway API installation
    ├── install-cilium/      # Cilium installation
    ├── configure-cilium-lb/ # LoadBalancer configuration
    ├── configure-gateway/   # Gateway configuration
    └── configure-node-roles/ # Node roles configuration
```

---

## ⚙️ Configuration

All settings are located in one file: `group_vars/all.yml`

### Main Parameters

```yaml
# Node IP addresses (REPLACE WITH YOUR ACTUAL IPs)
k8s_master_1_ip: "YOUR_MASTER_1_IP"  # Replace with your first master node IP
k8s_master_2_ip: "YOUR_MASTER_2_IP"  # Replace with your second master node IP
k8s_master_3_ip: "YOUR_MASTER_3_IP"  # Replace with your third master node IP

# Component versions
kubernetes_version: "1.34.1"
cilium_version: "1.18.3"
containerd_version: "2.1.4"
gateway_api_version: "v1.3.0"

# Network settings
pod_subnet: "10.244.0.0/16"
service_subnet: "10.96.0.0/12"
k8s_api_port: "6443"
```

See `group_vars/all.yml` for the complete list of parameters.

---

## 📋 Requirements

### System Requirements

- **OS**: Debian 12+ / Ubuntu 22.04+ / RHEL 9+
- **CPU**: Minimum 2 cores per node
- **RAM**: Minimum 4GB per node (8GB+ recommended)
- **Disk**: Minimum 20GB free space
- **Network**: Stable connection between nodes

### Node Requirements

- SSH access with keys (passwordless)
- sudo rights for Ansible user
- Open ports: 6443, 10250, 10259, 10257, 2379-2380, 8472

### Ansible Control Node Requirements

```bash
# Python 3.8+
python3 --version

# Ansible 2.9+
ansible --version

# Install dependencies
pip install ansible ansible-lint kubernetes
```

---

## 🔧 Usage

### Full Installation

```bash
cd k8s-install-ebpf-cilium
ansible-playbook playbooks/site.yml
```

### Step-by-Step Installation

```bash
# Step 1: System check
ansible-playbook playbooks/00-check-system.yml

# Step 2: Node preparation
ansible-playbook playbooks/01-prepare-nodes.yml

# Step 3: Cluster initialization
ansible-playbook playbooks/02-init-cluster.yml

# Step 4: Join master nodes
ansible-playbook playbooks/03-join-masters.yml

# Step 5: Install Gateway API
ansible-playbook playbooks/04-install-gateway-api.yml

# Step 6: Install Cilium
ansible-playbook playbooks/05-install-cilium.yml

# Step 7: Configure LoadBalancer
ansible-playbook playbooks/06-configure-cilium-lb.yml

# Step 8: Configure Gateway
ansible-playbook playbooks/07-configure-gateway.yml

# Step 9: Configure node roles
ansible-playbook playbooks/08-configure-node-roles.yml

# Step 10: Install CoreDNS
ansible-playbook playbooks/09-install-coredns.yml
```

### Cluster Verification

```bash
# On master-1 node
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get svc -A

# Check Cilium
cilium status
cilium connectivity test

# Check Gateway
kubectl get gateway -A
kubectl get gatewayclass
```

---

## 🎯 Best Practices

This project follows modern Ansible best practices 2025:

### 1. Using Modules Instead of shell/command

All tasks use specialized Ansible modules (`ansible.builtin.apt`, `kubernetes.core.k8s`) instead of direct `shell` or `command` calls, ensuring idempotency and better error handling.

### 2. Idempotency

All playbooks can be run multiple times without side effects. Tasks check system state before performing actions.

### 3. Centralized Variable Management

All variables are in `group_vars/all.yml` - a single source of truth for all configuration.

### 4. Modular Structure

The project uses Ansible roles to separate concerns and enable code reuse.

### 5. Kubernetes Best Practices

- HA Control Plane with 3 master nodes
- etcd in HA mode
- CoreDNS distributed with one replica per node (podAntiAffinity)
- Proper node labeling and taint usage

### 6. Cilium Best Practices

- kube-proxy replacement for better performance
- eBPF networking instead of iptables/IPVS
- Gateway API for modern ingress
- LoadBalancer IP Pool for IP address management

---

## 🔍 Troubleshooting

### Connection Check

```bash
# Check SSH connection
ansible all -m ping

# Check with verbose output
ansible all -m ping -vvv
```

### Syntax Check

```bash
# Check playbook syntax
ansible-playbook playbooks/site.yml --syntax-check

# Check ansible-lint
ansible-lint playbooks/ roles/
```

### Debug Execution

```bash
# Verbose output (level 3)
ansible-playbook playbooks/site.yml -vvv

# Execute single task
ansible-playbook playbooks/site.yml --tags "check-system"

# Check facts
ansible all -m setup
```

### Cluster Issues

```bash
# On master-1 node
# Check node status
kubectl get nodes -o wide

# Check pods
kubectl get pods -A -o wide

# Check events
kubectl get events --sort-by='.lastTimestamp' -A

# Component logs
kubectl logs -n kube-system <pod-name>
```

### Cilium Issues

```bash
# Check Cilium status
cilium status

# Check connectivity
cilium connectivity test

# Cilium logs
kubectl logs -n kube-system -l k8s-app=cilium

# Check eBPF programs
cilium bpf lb list
```

### Network Issues

```bash
# Check CNI
kubectl get pods -n kube-system | grep cilium

# Check LoadBalancer IP Pool
kubectl get ciliumloadbalancerippool

# Check Gateway
kubectl get gateway
kubectl get httproute
```

### Reinstall from Scratch

```bash
# On each node (CAREFUL!)
kubeadm reset -f
rm -rf /etc/cni/net.d
rm -rf /var/lib/etcd
rm -rf /etc/kubernetes

# Then run playbooks again
ansible-playbook playbooks/site.yml
```

---

## 📚 Documentation and Resources

### Official Documentation

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubeadm Documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
- [Cilium Documentation](https://docs.cilium.io/)
- [Cilium eBPF Networking](https://docs.cilium.io/en/stable/concepts/ebpf/)
- [Cilium kube-proxy Replacement](https://docs.cilium.io/en/stable/gettingstarted/kubeproxy-free/)
- [Gateway API Documentation](https://gateway-api.sigs.k8s.io/)
- [eBPF.io](https://ebpf.io/)

### Best Practices and Articles

- [Ansible Best Practices Guide 2025](https://medium.com/@devteam_40745/an-interactive-guide-to-ansible-best-practices-2025-7cfed8056e9a)
- [Kubernetes Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [Cilium Production Best Practices](https://docs.cilium.io/en/stable/operations/best-practices/)

### Communities

- [Ansible Community](https://www.ansible.com/community)
- [Kubernetes Slack](https://slack.k8s.io/)
- [Cilium Slack](https://cilium.io/slack)

---

## ⚠️ Important Notes

1. **IP Addresses Configuration**: 
   - **REQUIRED**: Before running the installation, you MUST replace all `YOUR_MASTER_X_IP` placeholders in `group_vars/all.yml` and `inventory/inventory.yml` with your actual node IP addresses.
   - IP addresses in both files must match exactly.
   - The IPs must be publicly accessible or reachable from your Ansible control node.

2. **Security**: Do not store secrets in plain text. Use Ansible Vault for sensitive data.

3. **Backup**: Before installing on production, make backups of all data.

4. **Testing**: Always test changes on a test environment before applying to production.

5. **Versions**: Check component version compatibility before updating.

6. **Network**: Ensure all required ports are open between nodes.

---

## 🎓 Usage Examples

### Create LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  labels:
    io.cilium/lb-ipam-layer2: "true"
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: my-app
```

### Create Gateway

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: gateway-system
spec:
  gatewayClassName: cilium
  listeners:
    - name: http
      protocol: HTTP
      port: 80
```

### Create HTTPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-route
  namespace: default
spec:
  parentRefs:
    - name: main-gateway
      namespace: gateway-system
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: your-service
          port: 80
```

---

## 📝 License

MIT License

---

## 🤝 Contributing

Contributions are welcome! Please create issues and pull requests.

---

**Created by Sergey Rytsev for Kubernetes cluster automation with eBPF/Cilium**

*Last updated: November 2025*
