# Production Kubernetes Cluster - Ansible Automation

Complete automation for deploying and configuring a production-ready Kubernetes cluster with IPVS, High Availability (HA), and modern best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Components](#components)
- [Security](#security)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## 📝 Overview

This project contains Ansible playbooks for automated installation and configuration of a production-ready Kubernetes cluster on Debian 13 (Trixie) nodes.

### Key Features

- ✅ **Kubernetes 1.34.1** with IPVS mode for high performance
- ✅ **Multiple master nodes** for highly available control plane (configurable)
- ✅ **kube-vip** for HA without external load balancer
- ✅ **Cilium CNI** for modern network policies
- ✅ **containerd** as container runtime
- ✅ **Helm** for application management
- ✅ **Complete security** (firewall, SSH hardening, audit)
- ✅ **Single configuration file** - edit only `cluster-config.yml`
- ✅ **Auto-generated inventory** - no manual inventory editing required

## 🔧 Requirements

### Prerequisites

1. **Ansible** >= 2.9 (recommended >= 2.14)
2. **Python** >= 3.8 on control machine (for inventory generator)
3. **PyYAML** package: `pip3 install pyyaml`
4. **SSH access** to all nodes with passwordless key-based authentication
5. **Root privileges** or passwordless sudo on all nodes
6. **Debian 13 (Trixie)** on all target nodes

### Environment Check

```bash
# Check Ansible version
ansible --version

# Check Python version (for inventory generator)
python3 --version

# Install PyYAML if needed
pip3 install pyyaml
```

## 🚀 Quick Start

### Step 1: Configure Your Cluster

**Edit ONLY one file: `cluster-config.yml`**

```bash
cd /path/to/kubernetes-ansible

# Copy example configuration (if cluster-config.yml doesn't exist)
cp cluster-config.yml.example cluster-config.yml

# Edit cluster configuration
vim cluster-config.yml  # or your preferred editor
```

Configure your master nodes:

```yaml
masters:
  - name: "k8s-master-1"
    ansible_host: "192.168.1.10"      # Your master node IP
    ansible_user: "root"                # SSH user
    vpn_ip: "10.0.0.1"                 # Optional: VPN/internal IP
  
  - name: "k8s-master-2"
    ansible_host: "192.168.1.11"
    ansible_user: "root"
    vpn_ip: "10.0.0.2"
  
  - name: "k8s-master-3"
    ansible_host: "192.168.1.12"
    ansible_user: "root"
    vpn_ip: "10.0.0.3"
```

Configure network settings:

```yaml
pod_network_cidr: "10.244.0.0/16"
service_network_cidr: "10.96.0.0/12"
control_plane_endpoint: "192.168.1.10:6443"
kube_vip_vip: "192.168.1.10"
```

### Step 2: Generate Inventory

```bash
# Generate inventory.yml from cluster-config.yml
python3 generate-inventory.py

# Verify generated inventory
cat inventory.yml
```

### Step 3: Test SSH Connectivity

```bash
# Test connectivity to all nodes
ansible all -m ping

# If connection fails, ensure SSH keys are set up:
# ssh-copy-id root@192.168.1.10  # Repeat for each node
```

### Step 4: Run Installation

```bash
# Full cluster installation (recommended)
ansible-playbook site.yml

# With verbose output
ansible-playbook site.yml -v

# With very verbose output (debugging)
ansible-playbook site.yml -vvv
```

### Step 5: Verify Installation

```bash
# Run cluster verification
ansible-playbook verify-cluster.yml

# Or manually check from first master
ansible k8s_masters[0] -m shell -a "kubectl get nodes"
```

## ⚙️ Configuration

### Single Configuration File

**All configuration is done in `cluster-config.yml`** - this is the ONLY file you need to edit!

### Configuration Sections

1. **Cluster Information**
   - `cluster_name`: Cluster identifier
   - `cluster_environment`: production, staging, development

2. **Master Nodes**
   - `masters`: List of master nodes with IPs and credentials
   - Each node can have `ansible_host`, `ansible_user`, `vpn_ip`

3. **Network Configuration**
   - `pod_network_cidr`: Pod network range
   - `service_network_cidr`: Service network range
   - `control_plane_endpoint`: Kubernetes API endpoint
   - `kube_vip_vip`: Virtual IP for HA

4. **Security**
   - `ssh_allowed_ips`: Networks allowed for SSH access
   - `firewall_enabled`: Enable/disable firewall
   - `public_ports`: Publicly accessible ports

5. **Component Versions**
   - `k8s_version`: Kubernetes version
   - `containerd_version`: containerd version
   - `cilium_version`: Cilium CNI version
   - `kube_vip_version`: kube-vip version
   - `helm_version`: Helm version

### Example Configuration

See `cluster-config.yml` for complete example with all available options.

### Auto-Generated Files

- `inventory.yml`: Generated from `cluster-config.yml` (DO NOT EDIT manually)
- Backup file `inventory.yml.backup` created automatically

## 📁 Project Structure

```
kubernetes-ansible/
├── cluster-config.yml              # ⭐ EDIT THIS FILE ONLY ⭐
├── generate-inventory.py            # Inventory generator script
├── inventory.yml                    # Auto-generated (DO NOT EDIT)
├── inventory.yml.example            # Example template
│
├── ansible.cfg                      # Ansible configuration
├── site.yml                         # Main playbook (entry point)
├── README.md                        # This documentation
│
├── kubernetes-install.yml           # Install components (all nodes)
├── kubernetes-init.yml              # Cluster initialization (first master)
├── kubernetes-join-masters.yml      # Join nodes (additional masters)
├── verify-cluster.yml               # Cluster verification
│
├── group_vars/
│   ├── all.yml                      # Global variables (uses cluster-config.yml)
│   └── k8s_masters.yaml             # Master nodes variables (auto-derived)
│
├── tasks/
│   ├── ipvs-masquerade-rules.yml    # IPVS masquerade and forward rules
│   └── scale-coredns.yml            # CoreDNS scaling configuration
│
└── roles/
    ├── containerd-configure/         # Configure containerd
    ├── kubernetes-repository/       # Add Kubernetes repository
    ├── kubernetes-install/          # Install kubelet, kubeadm, kubectl
    ├── helm-install/                # Install Helm
    ├── kube-vip-setup/              # Configure kube-vip for HA
    └── cilium-install/              # Install Cilium CNI
```

## 🎯 Usage

### Main Commands

```bash
# Full cluster installation (all stages sequentially)
ansible-playbook site.yml

# Only install components (without initialization)
ansible-playbook site.yml --tags install

# Only cluster initialization
ansible-playbook site.yml --tags init

# Only join additional nodes
ansible-playbook site.yml --tags join

# Only verification (without installation)
ansible-playbook verify-cluster.yml

# Skip verification
ansible-playbook site.yml --skip-tags verify
```

### Tags for Flexible Management

| Tag | Description |
|-----|-------------|
| `install` | Install components (containerd, k8s, helm) |
| `init` | Initialize cluster on first master |
| `join` | Join additional master nodes |
| `verify` | Verify cluster |
| `always` | Always executed (default) |

### Usage Examples

```bash
# Reinstall only components
ansible-playbook site.yml --tags install --force-handlers

# Re-initialize (with cleanup)
ansible k8s_masters[0] -m shell -a "kubeadm reset -f"
ansible-playbook site.yml --tags init

# Add another master
# 1. Edit cluster-config.yml (add new master)
# 2. Regenerate inventory: python3 generate-inventory.py
# 3. Join new master: ansible-playbook site.yml --tags join --limit k8s-master-new
```

## 📦 Components

### Component Versions (Configurable in cluster-config.yml)

| Component | Default Version | Config Variable |
|-----------|----------------|-----------------|
| Kubernetes | 1.34.1 | `k8s_version` |
| containerd | 2.1.3 | `containerd_version` |
| Cilium | 1.18.3 | `cilium_version` |
| kube-vip | 0.7.0 | `kube_vip_version` |
| Helm | 3.14.4 | `helm_version` |

### Operating Modes

- **kube-proxy**: IPVS (high performance) - configurable via `kube_proxy_mode`
- **kube-vip**: ARP mode, Layer 2 (without external LB) - configurable via `kube_vip_mode`
- **Cilium**: Native routing (without overlay)

## 🔒 Security

### SSH Access

SSH access is configured via `ssh_allowed_ips` in `cluster-config.yml`. By default, access is allowed from:

- VPN network (if configured)
- Master node IPs (auto-added)
- VPN server IP (if configured)
- Custom IPs you specify

### Firewall (UFW)

- **Default policy**: DENY (all incoming traffic blocked by default)
- **Full access** (all ports) for VPN network and trusted IPs
- **Public access** (only for other IPs): configured via `public_ports` in `cluster-config.yml`
- **Logging**: enabled for all blocks

### Additional Security

- ✅ SSH hardening (keys, IP restriction)
- ✅ fail2ban (brute-force protection)
- ✅ auditd (system audit)
- ✅ Automatic security patches (unattended-upgrades)

## ✅ Verification

### Automatic Verification

```bash
# Full cluster verification
ansible-playbook verify-cluster.yml

# Verification via Ansible ad-hoc
ansible k8s_masters[0] -m shell -a "kubectl get nodes"
ansible k8s_masters[0] -m shell -a "kubectl get pods -n kube-system"
```

### Manual Verification

```bash
# On first master
kubectl get nodes -o wide
kubectl get pods -n kube-system
kubectl get cs  # Component status

# Check IPVS
ipvsadm -Ln

# Check kube-proxy mode
kubectl get configmap kube-proxy -n kube-system -o yaml | grep mode

# Check VIP
curl -k https://<kube_vip_vip>:6443/healthz
```

## 🐛 Troubleshooting

### Issue: Cannot generate inventory

**Solution:**
```bash
# Install PyYAML
pip3 install pyyaml

# Verify cluster-config.yml syntax
python3 -c "import yaml; yaml.safe_load(open('cluster-config.yml'))"
```

### Issue: SSH unavailable after execution

**Solution:**
1. Check that you're connecting from allowed IP (configured in `cluster-config.yml`)
2. Check firewall rules: `ufw status numbered`
3. Check logs: `tail -f /var/log/ufw.log`

### Issue: kubeadm init fails

**Solution:**
```bash
# Cleanup and retry
ansible k8s_masters[0] -m shell -a "kubeadm reset -f"
ansible-playbook site.yml --tags init
```

### Issue: Node doesn't join cluster

**Solution:**
```bash
# Remove node from cluster (from first master)
kubectl delete node <node-name>

# Cleanup node
ansible <node-name> -m shell -a "kubeadm reset -f"

# Rejoin
ansible-playbook site.yml --tags join --limit <node-name>
```

### Issue: IPVS not active

**Solution:**
```bash
# Check kernel modules
lsmod | grep ip_vs

# Load modules
modprobe ip_vs
modprobe ip_vs_rr
modprobe ip_vs_wrr
modprobe ip_vs_sh

# Check kube-proxy configuration
kubectl get configmap kube-proxy -n kube-system -o yaml
```

### View Logs

```bash
# Ansible logs
tail -f ansible.log

# kubelet logs
journalctl -u kubelet -f

# kubeadm logs
journalctl -u kubelet | grep kubeadm

# Pod logs
kubectl logs -n kube-system <pod-name>
```

## 🔄 Workflow

### Typical Workflow

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd kubernetes-ansible
   ```

2. **Configure cluster**
   ```bash
   # Edit ONLY cluster-config.yml
   vim cluster-config.yml
   ```

3. **Generate inventory**
   ```bash
   python3 generate-inventory.py
   ```

4. **Verify connectivity**
   ```bash
   ansible all -m ping
   ```

5. **Install cluster**
   ```bash
   ansible-playbook site.yml
   ```

6. **Verify installation**
   ```bash
   ansible-playbook verify-cluster.yml
   ```

### Updating Configuration

1. Edit `cluster-config.yml`
2. Regenerate inventory: `python3 generate-inventory.py`
3. Re-run relevant playbooks or specific tags

## 📚 Additional Resources

### Official Documentation

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubeadm Installation Guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [High Availability Setup](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
- [IPVS Mode](https://kubernetes.io/docs/concepts/services-networking/service/#proxy-mode-ipvs)

### Components

- [Cilium Documentation](https://docs.cilium.io/)
- [kube-vip Documentation](https://kube-vip.io/)
- [Helm Documentation](https://helm.sh/docs/)

### Best Practices

- [Kubernetes Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

## 📝 Notes

### Important Notes

1. **Single Configuration File**: Edit ONLY `cluster-config.yml` for all configuration
2. **Auto-Generated Inventory**: `inventory.yml` is generated automatically (DO NOT EDIT)
3. **Idempotency**: Playbooks can be safely run multiple times
4. **Sequence**: Playbooks execute in specific order via `import_playbook`
5. **Tags**: Use tags for flexible installation management
6. **Logging**: All operations are logged in `ansible.log`
7. **Security**: After execution, SSH access is restricted to configured IPs

### Next Steps After Installation

1. **Monitoring Setup**: Install Prometheus + Grafana
2. **Logging**: Configure centralized logging (ELK, Loki)
3. **Backup**: Configure automatic etcd backup
4. **GitOps**: Setup Flux or ArgoCD
5. **Worker nodes**: Add worker nodes if needed

## 📄 License

This project is prepared for production use. All configurations follow Kubernetes and Ansible best practices.

---

**Version**: 3.0  
**Date**: November 2025  
**Maintained by**: Sergey Rytsev  
**Support**: Debian 13 (Trixie), Kubernetes 1.34.1
