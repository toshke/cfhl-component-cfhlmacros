import boto3

class NetworkLookup:

    def __init__(self):
        self.loaded = 0
        self.subnets = {}
        self.vpcs = {}

    def load(self):
        if self.loaded:
            return

        client = boto3.client('ec2')
        # load subnets
        subnets_r = client.describe_subnets()
        subnets_list = subnets_r['Subnets']
        while 'NextToken' in subnets_r:
            subnets_r = client.get_subnets(NextToken=subnets_r['NextToken'])
            subnets_list.extend(subnets_r['Subnets'])

        for subnet in subnets_list:
            name = None
            if 'Tags' in subnet:
                for tag in subnet['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            if name is not None:
                self.subnets[name] = subnet['SubnetId']

        # load vpcs
        vpcs_r = client.describe_vpcs()
        vpcs_list = vpcs_r['Vpcs']
        while 'NextToken' in vpcs_r:
            vpcs_r = client.describe_vpcs(NextToken=vpcs_r['NextToken'])
            vpcs_list.extend(vpcs_r['Subnets'])
        for vpc in vpcs_list:
            name = None
            if 'Tags' in vpc:
                for tag in vpc['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            if name is not None:
                self.vpcs[name] = vpc['VpcId']

    def get_subnets(self, environment_name, subnetname):
        self.load()
        return list(map( lambda x: self.subnets[x] ,
                         filter(lambda x: x.startswith(f"{environment_name}{subnetname}"), self.subnets)
        ))

nl = NetworkLookup()

def replace_subnets(value, parameters):
    if isinstance(value, str) and value.startswith('CfHl.Subnet'):
        parts = value.split('.')
        if len(parts) == 3:
            subnet_class = parts[2]
            environment_name = parameters['EnvironmentName']
            subnets = nl.get_subnets(environment_name, subnet_class)
            if parts[1] == 'Subnets':
                return subnets
            elif parts[1] == 'Subnet':
                if subnets:
                    return subnets[0]
    return value

def replace_vpc(value, parameters):
    if isinstance(value, str) and value.startswith('CfHl.Vpc'):
        nl.load()
        parts = value.split('.')
        environment_name = parameters['EnvironmentName']
        if len(parts) == 3:
            prop = parts[2]
            if prop == 'Id':
                vpcs = nl.vpcs
                if f"{environment_name}-vpc" in vpcs:
                    return vpcs[f"{environment_name}-vpc"]
    return value

def replace_network(value, parameters):
    value = replace_subnets(value, parameters)
    value = replace_vpc(value, parameters)
    return value

if __name__ == '__main__':
    print(replace_network('CfHl.Subnets.Public',{'EnvironmentName':'dev'}))
    print(replace_network('CfHl.Subnet.Public0',{'EnvironmentName':'dev'}))
    print(replace_network('CfHl.Vpc.Id',{'EnvironmentName':'dev'}))
