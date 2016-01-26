# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "debian/jessie64"
  config.vm.network "public_network"
  config.vbguest.auto_update = false

  config.vm.define "internal1" do |web|
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "internal1"
    end
  end

  config.vm.define "internal2" do |web|
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.name = "internal2"
    end
  end

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      "galaxie" => ["internal1", "internal2"],
      "all_groups:children" => ["galaxie"]
    }
    ansible.playbook = "alfred-install.yml"
  end
end
