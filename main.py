from cdktf import App
from variables import NetworkConfig
from stacks.NetworkStack import NetworkStack
from stacks.InstanceStack import InstanceStack

def main():
    app = App()
    config = NetworkConfig()

    # Create stacks
    network = NetworkStack(app, "network", config)
    instance = InstanceStack(app, "instance", config, network)

    # Add explicit dependency for instance
    instance.add_dependency(network)

    app.synth()

if __name__ == "__main__":
    main()
