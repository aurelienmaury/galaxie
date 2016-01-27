# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "debian/jessie64"
  config.vm.network "public_network", bridge: "en1: Wi-Fi (AirPort)"
  config.vbguest.auto_update = false

  config.vm.define "internal_1" do |web|
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "internal_1"
    end
  end

  config.vm.define "internal_2" do |web|
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "internal_2"
    end

    config.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.groups = {
        "galaxie" => ["internal_1", "internal_2"],
        "apt-cacher-ng-server" => ["internal_2"],
        "openssh-client" => ["internal_1", "internal_2"],
        "openssh-server" => ["internal_1", "internal_2"],
        "ntp-clients" => ["internal_1"],
        "ntp-servers" => ["internal_2"],
        "servers:children" => ["ntp-servers", "apt-cacher-ng-server"],
        "galaxie:children" => ["servers"],
        "all_groups:children" => ["galaxie"]
      }
      ansible.playbook = "playbooks/vagrant-provision.yml"
    end
  end


end
