#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by amazon_cloud_code_generator.
# See: https://github.com/ansible-collections/amazon_cloud_code_generator

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: ec2_vpc
short_description: Create and manage AWS virtual private clouds (VPCs)
description: Create and manage AWS VPCs (list, create, update, describe, delete).
options:
    cidr_block:
        description:
        - The primary IPv4 CIDR block for the VPC.
        required: true
        type: str
    enable_dns_hostnames:
        description:
        - Indicates whether the instances launched in the VPC get DNS hostnames.
        - If enabled, instances in the VPC get DNS hostnames; otherwise, they do not.
        - Disabled by default for nondefault VPCs.
        type: bool
    enable_dns_support:
        description:
        - Indicates whether the DNS resolution is supported for the VPC. If enabled,
            queries to the Amazon provided DNS server at the 169.254.169.253 IP address,
            or the reserved IP address at the base of the VPC network range plus two
            succeed.
        - If disabled, the Amazon provided DNS service in the VPC that resolves public
            DNS hostnames to IP addresses is not enabled.
        - Enabled by default.
        type: bool
    instance_tenancy:
        description:
        - The allowed tenancy of instances launched into the VPC.
        - 'default: An instance launched into the VPC runs on shared hardware by default,
            unless you explicitly specify a different tenancy during instance launch.'
        - 'dedicated: An instance launched into the VPC is a Dedicated Instance by
            default, unless you explicitly specify a tenancy of host during instance
            launch.'
        - You cannot specify a tenancy of default during instance launch.
        - Updating I(instance_tenancy) requires no replacement only if you are updating
            its value from dedicated to default.
        - Updating I(instance_tenancy) from default to dedicated requires replacement.
        type: str
    state:
        choices:
        - create
        - update
        - delete
        - list
        - describe
        - get
        default: create
        description:
        - Goal state for resouirce.
        - I(state=create) creates the resouce.
        - I(state=update) updates the existing resouce.
        - I(state=delete) ensures an existing instance is deleted.
        - I(state=list) get all the existing resources.
        - I(state=describe) or I(state=get) retrieves information on an existing resource.
        type: str
    tags:
        description:
        - The tags for the VPC.
        elements: dict
        suboptions:
            key:
                required: true
                type: str
            value:
                required: true
                type: str
        type: list
    vpc_id:
        description:
        - The Id for the model.
        type: str
    wait:
        default: false
        description:
        - Wait for operation to complete before returning.
        type: bool
    wait_timeout:
        default: 320
        description:
        - How many seconds to wait for an operation to complete before timing out.
        type: int
author: Ansible Cloud Team (@ansible-collections)
version_added: TODO
requirements: []
"""

EXAMPLES = r"""
"""

RETURN = r"""
result:
    identifier:
        description: The unique identifier of the resource.
        type: str
    properties:
        description: The resource properties.
        type: complex
"""

import json

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.utils import (
    snake_dict_to_camel_dict,
)


def main():

    argument_spec = dict(
        client_token=dict(type="str", no_log=True),
        state=dict(
            type="str",
            choices=["create", "update", "delete", "list", "describe", "get"],
            default="create",
        ),
    )

    argument_spec["vpc_id"] = {"type": "str"}
    argument_spec["cidr_block"] = {"type": "str", "required": True}
    argument_spec["enable_dns_hostnames"] = {"type": "bool"}
    argument_spec["enable_dns_support"] = {"type": "bool"}
    argument_spec["instance_tenancy"] = {"type": "str"}
    argument_spec["tags"] = {
        "type": "list",
        "elements": "dict",
        "suboptions": {
            "key": {"type": "str", "required": True},
            "value": {"type": "str", "required": True},
        },
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "update", "delete", "list", "describe", "get"],
        "default": "create",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}

    required_if = [
        ["state", "update", ["vpc_id"], True],
        ["state", "delete", ["vpc_id"], True],
        ["state", "get", ["vpc_id"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::EC2::VPC"

    params = {}

    params["cidr_block"] = module.params.get("cidr_block")
    params["enable_dns_hostnames"] = module.params.get("enable_dns_hostnames")
    params["enable_dns_support"] = module.params.get("enable_dns_support")
    params["instance_tenancy"] = module.params.get("instance_tenancy")
    params["tags"] = module.params.get("tags")
    params["vpc_id"] = module.params.get("vpc_id")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}
    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    desired_state = json.dumps(params_to_set)
    state = module.params.get("state")
    identifier = module.params.get("vpc_id")

    results = {"changed": False, "result": []}

    if state == "list":
        results["result"] = cloud.list_resources(type_name)

    if state in ("describe", "get"):
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "create":
        results["changed"] |= cloud.create_resource(
            type_name, identifier, desired_state
        )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "update":
        # Ignore createOnlyProperties that can be set only during resource creation
        create_only_params = ["cidr_block"]
        results["changed"] |= cloud.update_resource(
            type_name, identifier, params_to_set, create_only_params
        )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "delete":
        results["changed"] |= cloud.delete_resource(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()
