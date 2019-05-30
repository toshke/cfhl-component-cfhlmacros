import boto3

class SubnetLookup:

    def __init__(self):
        self.loaded = 0
        self.subnets = {}

    def _load_subnets(self):
        if self.loaded:
            return

        client = boto3.client('ec2')
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

    def get_subnets(self, environment_name, subnetname):
        self._load_subnets()
        return list(map( lambda x: self.subnets[x] ,
                         filter(lambda x: x.startswith(f"{environment_name}{subnetname}"), self.subnets)
        ))

    sl = SubnetLookup()
    def replace_subnets(value, parameters):
        if isinstance(value, str) and value.startswith('CfHl.Subnet'):
            parts = value.split('.')
            if len(parts) == 3:
                subnet_class = parts[2]
                environment_name = parameters['EnvironmentName']
                subnets = sl.get_subnets(environment_name, subnet_class)
                if parts[1] == 'Subnets':
                    return subnets
                elif parts[1] == 'Subnet':
                    if subnets:
                        return subnets[0]
        return value
