#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_containerregistry_facts
version_added: "2.5"
short_description: Get Registry facts.
description:
    - Get facts of Registry.

options:
    resource_group:
        description:
            - The name of the resource group to which the container registry belongs.
        required: True
    registry_name:
        description:
            - The name of the container registry.
    format:
        description:
            - Format of the data returned.
            - If C(raw) is selected information will be returned in raw format from Azure Python SDK.
            - If C(curated) is selected the structure will be identical to input parameters of azure_rm_virtualmachine_scaleset module.
            - In Ansible 2.5 and lower facts are always returned in raw format.
        default: 'raw'
        choices:
            - 'curated'
            - 'raw'

extends_documentation_fragment:
    - azure

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of Registry
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
      registry_name: registry_name

  - name: List instances of Registry
    azure_rm_containerregistry_facts:
      resource_group: resource_group_name
'''

RETURN = '''
registries:
    description: A list of dict results where the key is the name of the Registry and the values are the facts for that Registry.
    returned: always
    type: complex
    contains:
        registry_name:
            description: The key is the name of the server that the values relate to.
            type: complex
            contains:
                id:
                    description:
                        - The resource ID.
                    returned: always
                    type: str
                    sample: "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.ContainerRegistry/registr
                            ies/myRegistry"
                name:
                    description:
                        - The name of the resource.
                    returned: always
                    type: str
                    sample: myRegistry
                type:
                    description:
                        - The type of the resource.
                    returned: always
                    type: str
                    sample: Microsoft.ContainerRegistry/registries
                location:
                    description:
                        - The location of the resource. This cannot be changed after the resource is created.
                    returned: always
                    type: str
                    sample: westus
                sku:
                    description:
                        - The SKU of the container registry.
                    returned: always
                    type: complex
                    sample: sku
                    contains:
                        name:
                            description:
                                - "The SKU name of the container registry. Required for registry creation. Possible values include: 'Classic', 'Basic', 'Stan
                                  dard', 'Premium'"
                            returned: always
                            type: str
                            sample: Standard
                        tier:
                            description:
                                - "The SKU tier based on the SKU name. Possible values include: 'Classic', 'Basic', 'Standard', 'Premium'"
                            returned: always
                            type: str
                            sample: Standard
                status:
                    description:
                        - The status of the container registry at the time the operation was called.
                    returned:
                    type: complex
                    sample: status
                    contains:
                        message:
                            description:
                                - The detailed message for the status, including alerts and error messages.
                            returned: always
                            type: str
                            sample: The registry is ready.
                        timestamp:
                            description:
                                - The timestamp when the status was changed to the current value.
                            returned: always
                            type: datetime
                            sample: "2017-03-01T23:15:37.0707808Z"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.containerregistry import ContainerRegistryManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMRegistriesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            registry_name=dict(
                type='str'
            ),
            format=dict(
                type='str',
                choices=['curated',
                         'raw'],
                default='raw'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
        )
        self.mgmt_client = None
        self.resource_group = None
        self.registry_name = None
        self.format = None
        super(AzureRMRegistriesFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(ContainerRegistryManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.registry_name is not None):
            self.results['registries'] = self.get()
        elif (self.resource_group is not None):
            self.results['registries'] = self.list_by_resource_group()
        return self.results

    def get(self):
        response = None
        results = {}
        try:
            response = self.mgmt_client.registries.get(resource_group_name=self.resource_group,
                                                       registry_name=self.registry_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            results[response.name] = self.format_item(response)

        return results

    def list_by_resource_group(self):
        response = None
        results = {}
        try:
            response = self.mgmt_client.registries.list_by_resource_group(resource_group_name=self.resource_group)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Registries.')

        if response is not None:
            for item in response:
                results[item.name] = self.format_item(item)

        return results

    def format_item(self, item):
        d = item.as_dict()
        if self.format == 'curated':
            d = {
                'resource_group': self.resource_group,
                'name': self.registry_name,
                'location': d['location'],
                'admin_user_enabled': d['admin_user_enabled'],
                'sku': d['sku']['tier'].lower(),
                'state': 'present'
            }
        return d


def main():
    AzureRMRegistriesFacts()
if __name__ == '__main__':
    main()
