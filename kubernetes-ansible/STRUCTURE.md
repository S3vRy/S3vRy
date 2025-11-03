# Project Structure and Configuration Guide

## 🎯 Single Configuration File Approach

This project uses a **single configuration file** approach. You only need to edit **ONE file** to configure your entire Kubernetes cluster.

### Configuration File: `cluster-config.yml`

This is the **ONLY file you need to edit** to configure your cluster. All other files use variables from this configuration.

## 📁 File Structure

### Configuration Files

```
cluster-config.yml              # ⭐ EDIT THIS FILE ONLY ⭐
├── Cluster information (name, environment)
├── Master nodes configuration
├── Network configuration
├── Security settings
├── Component versions
└── System settings
```

### Auto-Generated Files

```
inventory.yml                   # Generated from cluster-config.yml
├── DO NOT EDIT manually
├── Regenerate with: python3 generate-inventory.py
└── Automatically backed up before regeneration
```

### Playbooks

```
site.yml                       # Main playbook (entry point)
├── Loads cluster-config.yml
├── Orchestrates all stages
└── Tags for flexible execution

kubernetes-install.yml          # Stage 1: Install components
kubernetes-init.yml             # Stage 2: Initialize cluster
kubernetes-join-masters.yml    # Stage 3: Join additional masters
verify-cluster.yml              # Stage 4: Verify installation
```

### Variable Files

```
group_vars/
├── all.yml                    # Global variables (uses cluster-config.yml)
└── k8s_masters.yaml           # Master nodes variables (auto-derived)
```

### Scripts

```
generate-inventory.py           # Generate inventory.yml from cluster-config.yml
└── Requirements: Python 3.8+, PyYAML
```

### Templates and Examples

```
inventory.yml.example           # Example inventory template
examples/
└── kubeadm-config-ipvs.yaml   # Example kubeadm config
```

## 🔄 Workflow

### 1. Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd kubernetes-ansible

# 2. Edit ONLY cluster-config.yml
vim cluster-config.yml

# 3. Generate inventory
python3 generate-inventory.py

# 4. Verify connectivity
ansible all -m ping

# 5. Install cluster
ansible-playbook site.yml
```

### 2. Updating Configuration

```bash
# 1. Edit cluster-config.yml
vim cluster-config.yml

# 2. Regenerate inventory (if nodes changed)
python3 generate-inventory.py

# 3. Re-run playbooks
ansible-playbook site.yml
```

## 📝 Configuration Sections

### Cluster Information

```yaml
cluster_name: "production-k8s"
cluster_environment: "production"
```

### Master Nodes

```yaml
masters:
  - name: "k8s-master-1"
    ansible_host: "192.168.1.10"
    ansible_user: "root"
    vpn_ip: "10.0.0.1"  # Optional
```

### Network Configuration

```yaml
pod_network_cidr: "10.244.0.0/16"
service_network_cidr: "10.96.0.0/12"
control_plane_endpoint: "192.168.1.10:6443"
kube_vip_vip: "192.168.1.10"
```

### Security

```yaml
ssh_allowed_ips:
  # Master node IPs are auto-added
  # Add custom IPs here if needed
  
firewall_enabled: true
public_ports:
  - "80/tcp"
  - "443/tcp"
```

### Component Versions

```yaml
k8s_version: "1.34.1"
containerd_version: "2.1.3"
cilium_version: "1.18.3"
kube_vip_version: "0.7.0"
helm_version: "3.14.4"
```

## 🔐 Security Notes

- **inventory.yml** is auto-generated and should NOT be committed to Git
- **cluster-config.yml** contains sensitive information - consider encrypting or using Ansible Vault
- SSH keys must be set up for passwordless access
- Firewall rules are automatically configured based on `ssh_allowed_ips`

## 🛠 Maintenance

### Adding a New Master Node

1. Edit `cluster-config.yml` - add new master to `masters` list
2. Run `python3 generate-inventory.py`
3. Ensure SSH access to new node
4. Run `ansible-playbook site.yml --tags join --limit <new-node-name>`

### Updating Component Versions

1. Edit `cluster-config.yml` - update version variables
2. Run `ansible-playbook site.yml --tags install`

### Changing Network Configuration

1. Edit `cluster-config.yml` - update network CIDRs
2. Run `ansible-playbook site.yml` (will re-configure networking)

## 📚 Best Practices

1. **Version Control**: Commit `cluster-config.yml.example` but NOT `cluster-config.yml` (contains your specific config)
2. **Backups**: The inventory generator automatically backs up existing `inventory.yml`
3. **Testing**: Test configuration changes on a staging environment first
4. **Documentation**: Document any custom changes in comments within `cluster-config.yml`

## ⚠️ Important Notes

- **DO NOT** edit `inventory.yml` manually - it will be overwritten
- **DO NOT** edit files in `group_vars/` directly - they use variables from `cluster-config.yml`
- **DO** keep `cluster-config.yml` in version control (consider encrypting sensitive data)
- **DO** regenerate inventory after changing master nodes in `cluster-config.yml`

