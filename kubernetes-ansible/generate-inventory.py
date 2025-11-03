#!/usr/bin/env python3
"""
Generate inventory.yml from cluster-config.yml
Run this script before executing ansible-playbook site.yml

Usage:
    python3 generate-inventory.py
"""

import yaml
import sys
import os
from pathlib import Path

def load_config(config_path):
    """Load cluster configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found!")
        print("Please create cluster-config.yml based on cluster-config.yml.example")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse '{config_path}': {e}")
        sys.exit(1)

def generate_inventory(config):
    """Generate Ansible inventory from configuration"""
    inventory = {
        'all': {
            'children': {
                'k8s_masters': {
                    'hosts': {},
                    'vars': {
                        'node_role': 'master'
                    }
                }
            }
        }
    }

    # Add master nodes
    masters = config.get('masters', [])
    if not masters:
        print("Error: No masters defined in cluster-config.yml")
        sys.exit(1)

    for master in masters:
        master_config = {
            'ansible_host': master.get('ansible_host'),
            'ansible_user': master.get('ansible_user', config.get('ansible_user', 'root'))
        }
        if 'vpn_ip' in master:
            master_config['vpn_ip'] = master['vpn_ip']
        
        inventory['all']['children']['k8s_masters']['hosts'][master['name']] = master_config

    # Add VPN server if configured
    vpn_server_ip = config.get('vpn_server_ip')
    if vpn_server_ip:
        vpn_network = config.get('vpn_network', '10.0.0.0/24')
        vpn_base_ip = vpn_network.split('/')[0].rsplit('.', 1)[0] + '.10'
        
        inventory['all']['children']['vpn_server'] = {
            'hosts': {
                'vpn-server': {
                    'ansible_host': vpn_server_ip,
                    'ansible_user': config.get('ansible_user', 'root'),
                    'vpn_ip': vpn_base_ip
                }
            }
        }

    return inventory

def backup_existing_inventory(inventory_path):
    """Backup existing inventory file if it exists"""
    if inventory_path.exists():
        backup_path = inventory_path.with_suffix('.yml.backup')
        import shutil
        shutil.copy2(inventory_path, backup_path)
        print(f"Backed up existing inventory to {backup_path}")

def main():
    script_dir = Path(__file__).parent
    config_path = script_dir / 'cluster-config.yml'
    inventory_path = script_dir / 'inventory.yml'

    print(f"Loading configuration from {config_path}...")
    config = load_config(config_path)

    print(f"Generating inventory file...")
    inventory = generate_inventory(config)

    # Backup existing inventory
    backup_existing_inventory(inventory_path)

    # Write inventory file
    try:
        with open(inventory_path, 'w') as f:
            yaml.dump(inventory, f, default_flow_style=False, sort_keys=False)
        print(f"✓ Inventory file generated successfully: {inventory_path}")
        print(f"\nMaster nodes configured: {len(config.get('masters', []))}")
        for master in config.get('masters', []):
            print(f"  - {master['name']}: {master.get('ansible_host')}")
        if config.get('vpn_server_ip'):
            print(f"\nVPN server: {config.get('vpn_server_ip')}")
    except IOError as e:
        print(f"Error: Failed to write inventory file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

