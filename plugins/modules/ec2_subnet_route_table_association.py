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
module: ec2_subnet_route_table_association
short_description: []
description: []
options:
    id:
        type: str
    route_table_id:
        required: true
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
    subnet_id:
        required: true
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

    argument_spec["id"] = {"type": "str"}
    argument_spec["route_table_id"] = {"type": "str", "required": True}
    argument_spec["subnet_id"] = {"type": "str", "required": True}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "update", "delete", "list", "describe", "get"],
        "default": "create",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}

    required_if = [
        ["state", "create", ["id", "route_table_id", "subnet_id"], True],
        ["state", "update", ["id"], True],
        ["state", "delete", ["id"], True],
        ["state", "get", ["id"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::EC2::SubnetRouteTableAssociation"

    params = {}

    params["id"] = module.params.get("id")
    params["route_table_id"] = module.params.get("route_table_id")
    params["subnet_id"] = module.params.get("subnet_id")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}
    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    desired_state = json.dumps(params_to_set)
    state = module.params.get("state")
    identifier = module.params.get("id")

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
        create_only_params = ["/properties/SubnetId", "/properties/RouteTableId"]
        results["changed"] |= cloud.update_resource(
            type_name, identifier, params_to_set, create_only_params
        )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "delete":
        results["changed"] |= cloud.delete_resource(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()
